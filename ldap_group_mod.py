#!/usr/bin/python
import ldap
import sys

if len(sys.argv) != 4:
	print "Usage: ", sys.argv[0], "<group> ADD|REMOVE <user>"
	exit(1)

group = sys.argv[1]
op_type = sys.argv[2]
member_type = "memberUid"
user = sys.argv[3]

con = ldap.initialize("ldap://example.com")

con.simple_bind_s("cn=admin,dc=example,dc=com", "AdMiNPa$$w0rD")

res = con.search_s("ou=group,dc=example,dc=com", ldap.SCOPE_SUBTREE, "cn=%s" % group, ['Name', 'memberUid'])


for dn,entry in res:
	if entry['cn'][0] != group:
		continue
	if op_type == "REMOVE":
		mod_attrs = [(ldap.MOD_DELETE, member_type, user)]
	if op_type == "ADD":
		mod_attrs = [(ldap.MOD_ADD, member_type, user)]
	con.modify_s(dn, mod_attrs)
con.unbind()
