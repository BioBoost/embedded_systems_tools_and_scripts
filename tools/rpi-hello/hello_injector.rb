#!/usr/bin/env ruby

require 'fileutils'

class FileNotFound < Exception; end
class BlockSizeNotFound < Exception; end
class RootPartitionOffsetNotFound < Exception; end
class MountDirShouldBeEmpty < Exception; end
class CouldNotMountImage < Exception; end
class CouldNotUnmountImage < Exception; end

class HelloInjector
  SERVICE_SCRIPT_NAME = 'rpi-hello.service'
  HELLO_RPI_DESTINATION_DIR = "/usr/local/share/"
  SYSTEMD_SERVICE_SYMLINK_TARGET_DIR = "/etc/systemd/system/multi-user.target.wants/"
  IMAGE_CLONE_PATH = "/tmp/"

  def initialize image_file, hello_rpi_path, mount_directory="/tmp/rpi_linux_image"
    # Some sanity checks
    raise FileNotFound.new("Image file #{image_file} does not exist") unless File.exists?(image_file)
    raise FileNotFound.new("Directory #{hello_rpi_path} does not exist") unless File.exists?(hello_rpi_path)

    systemd_service_script = File.join(hello_rpi_path, 'service', SERVICE_SCRIPT_NAME)
    raise FileNotFound.new("Systemd service script file #{systemd_service_script} does not exist") unless File.exists?(systemd_service_script)

    @image_file = image_file
    @hello_rpi_path = hello_rpi_path
    @mount_directory = mount_directory

  end

  def inject
    create_image_copy
    determine_mount_offset
    mount_rootfs_partition

    copy_rpi_hello_to_rootfs
    symlink_systemd_service

    puts "Press any key to finish and unmount"
    gets

    unmount_rootfs_partition

    puts "Your altered image is available at #{@image_file}"
  end

  private
  def create_image_copy
    new_image_file = File.join(IMAGE_CLONE_PATH, @image_file.split('/').last)
    puts "Copying image #{@image_file} to #{new_image_file}"
    is_success = system("sudo cp #{@image_file} #{new_image_file}")
    @image_file = new_image_file
    puts "Succesfully copied" if is_success
  end

  def determine_mount_offset
    fdisk_info = get_fdisk_info
    blocksize = get_block_size fdisk_info
    rootfs_partition_start = get_rootfs_partition_start fdisk_info
    @mount_offset = blocksize.to_i * rootfs_partition_start.to_i
  end

  def get_fdisk_info
    fdisk_output = `fdisk -l #{@image_file}`
  end

  def get_block_size fdisk_info
    info_match = /Units.*?(\d+)\sbytes/.match(fdisk_info)
    raise BlockSizeNotFound.new("Could not match blocksize") if info_match.nil?
    info_match[1]
  end

  def get_rootfs_partition_start fdisk_info
    info_match = /^.*?img2\s+(\d+)\s+.*/.match(fdisk_info)
    raise RootPartitionOffsetNotFound.new("Could not match rootfs partition offset") if info_match.nil?
    info_match[1]
  end

  def mount_rootfs_partition
    prepare_mount_directory
    is_success = system("sudo mount -o loop,offset=#{@mount_offset} #{@image_file} #{@mount_directory}")
    raise CouldNotMountImage.new unless is_success
    puts "File system succesfully mounted at: #{@mount_directory}"
  end

  def prepare_mount_directory
    @remove_mount_dir = false
    unless Dir.exists?(@mount_directory)
      Dir.mkdir(@mount_directory)
      @remove_mount_dir = true 
    end
    raise MountDirShouldBeEmpty.new unless (Dir.entries(@mount_directory) - %w{ . .. }).empty?
  end

  def unmount_rootfs_partition
    system("sudo sync")
    is_success = system("sudo umount #{@mount_directory}")
    cleanup_mount_directory
    raise CouldNotUnmountImage.new unless is_success
    puts "File system succesfully unmounted"
  end

  def cleanup_mount_directory
    Dir.rmdir(@mount_directory) if @remove_mount_dir
  end

  def copy_rpi_hello_to_rootfs
    sourceDir = @hello_rpi_path

    if HELLO_RPI_DESTINATION_DIR[0] == '/'
      relativeDestinationPath = HELLO_RPI_DESTINATION_DIR[1..-1]
    else
      relativeDestinationPath = HELLO_RPI_DESTINATION_DIR
    end

    mountedDestinationDir = File.join(@mount_directory, relativeDestinationPath)

    puts "Copying #{sourceDir} to #{mountedDestinationDir}"
    is_success = system("sudo cp -r #{sourceDir} #{mountedDestinationDir}")
    puts "rpi hello dir succesfully copied to rootfs" if is_success
  end

  def symlink_systemd_service
    if SYSTEMD_SERVICE_SYMLINK_TARGET_DIR[0] == '/'
      relativeLinkname = SYSTEMD_SERVICE_SYMLINK_TARGET_DIR[1..-1]
    else
      relativeLinkname = SYSTEMD_SERVICE_SYMLINK_TARGET_DIR
    end

    target = File.join(HELLO_RPI_DESTINATION_DIR, @hello_rpi_path.split('/').last, 'service', 'rpi-hello.service')
    linkname = File.join(@mount_directory, relativeLinkname, 'rpi-hello.service')

    puts "Creating symlink #{linkname} for target #{target}"
    is_success = system("sudo ln -f -s #{target} #{linkname}")
    puts "succesfully created symlink" if is_success
  end

end


# Here you can alter where the image is located and where your rpi-project is located
injector = HelloInjector.new "/home/bioboost/Downloads/2016-05-27-raspbian-jessie-lite.img", "/media/sf_VM_MINTYFRESH/rpi-hello"
injector.inject
puts "done"