# Construct ACL command for packet capture filter

def acl_command(proto,src,dst):
    if (src == 'any') and (dst == 'any'):
        configuration = '''ip access-list extended PKT_CAP
                           permit %s %s %s''' %(proto,src,dst)
    elif (src == 'any') and (dst != 'any'):
        configuration = '''ip access-list extended PKT_CAP
                           permit %s %s host %s''' %(proto,src,dst)
    elif (src != 'any') and (dst != 'any'):
        configuration = '''ip access-list extended PKT_CAP
                           permit %s host %s %s''' %(proto,src,dst)
    else:
        configuration = '''ip access-list extended PKT_CAP
                           permit %s host %s host %s''' %(proto,src,dst)

    return configuration