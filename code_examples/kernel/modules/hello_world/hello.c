#include <linux/init.h>     // Macros used to mark up functions e.g. __init and __exit
#include <linux/module.h>   // Core header for loading LKMs into the kernel
#include <linux/kernel.h>   // Contains types, macros, functions for the kernel

MODULE_LICENSE("GPL");            // License type; effect runtime behavior
                                  // Kernel may be marked as tained when "Proprietary"
MODULE_AUTHOR("Nico De Witte");   // Visible when using modinfo
MODULE_DESCRIPTION("Simple Hello World for RPI2");
MODULE_VERSION("0.1");

static char *name = "Universe";   // Argument -- default is Universe
module_param(name, charp, S_IRUGO);   // Param description 
                                      // charp = char ptr
                                      // S_IRUGO = Read User, Group, Others
MODULE_PARM_DESC(name, "The name you want this module to address");

/**
 * Initialization function (called when loading the module)
 * The static keyword restricts scope of the function to this C file.
 * The __init macro states that for built-in driver (not LKM!) the function
 * is only used at initialization time and can be discarded and its memory freed up
 * after that point.
 */
static int __init hello_init(void)
{
  printk(KERN_INFO "NDW: Hello %s from Kernel Space\n", name);
  return 0;
}

/**
 * Exit function
 * Similar to init function
 * __exit macro states that if this is built-in driver (not LKM!) the function
 * is not required.
 * NDW: Does this mean it is not called for built-in ? May have serious implications !
 */
static void __exit hello_exit(void)
{
  printk(KERN_INFO "NDW: ByeBye %s from Kernel Space\n", name);
}

//  Identify the init and exit functions
module_init(hello_init);
module_exit(hello_exit);