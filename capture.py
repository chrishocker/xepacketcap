# functions to set up, start, and stop packet capture in XE device
# note - may need to change syntax of export command for CSR

import cli

def acl_command(proto,src,dst):
    if (src == 'any') and (dst == 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s %s %s''' %(proto,src,dst)
    elif (src == 'any') and (dst != 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s %s host %s''' %(proto,src,dst)
    elif (src != 'any') and (dst != 'any'):
        command = '''ip access-list extended PKT_CAP
                           permit %s host %s %s''' %(proto,src,dst)
    else:
        command = '''ip access-list extended PKT_CAP
                           permit %s host %s host %s''' %(proto,src,dst)

    return command


def start_capture(proto,src,dst):
    configuration = acl_command(proto, src, dst)
    cli.configure(configuration)
    cli.execute(
        "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
    cmd = "monitor capture PKT_CAP interface %s both" % args.interface
    cli.execute(cmd)
    cli.execute("monitor capture PKT_CAP clear")
    cli.execute("monitor capture PKT_CAP start")


def cap_cleanup():
    cli.execute("monitor capture PKT_CAP stop")
    cmd = "monitor capture PKT_CAP export location flash:%s" % filename  # changed syntax to fit Cat9K
    cli.execute(cmd)
    configuration = 'no ip access-list extended PKT_CAP'  # delete capture ACL so next capture has a fresh filter
    cli.configure(configuration)