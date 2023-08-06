from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE
import json


class Member:
    def __init__(self, ine="", utt_login="", utt_id_number=""):
        server = Server('ldap.utt.fr', get_info=ALL)
        base_dn = "ou=people,dc=utt,dc=fr"
        connection = Connection(server, auto_bind=True)
        query = ""
        if len(ine) > 0:
            query += "(supannCodeINE=" + ine + ")"
        if len(utt_login) > 0:
            query += "(uid=" + utt_login + ")"
        if len(utt_id_number) > 0:
            query += "(supannempid=" + utt_id_number + ")"
        if len(query) > 0 and connection.search(base_dn, "(&(objectClass=person)" + query+")", attributes=ALL_ATTRIBUTES,
                                                search_scope=SUBTREE):
            member = json.loads(connection.entries[0].entry_to_json())["attributes"]

            self.given_name = " ".join(
                [j.capitalize() for j in
                 "-".join([i.capitalize() for i in member["givenName"][0].split("-")]).split(" ")])
            self.last_name = member["sn"][0].upper()
            self.full_name = self.given_name + " " + self.last_name

            self.login = member['uid'][0]
            self.number_id = member["supannEmpId"][0]
            self.ine = member.get("supannCodeINE", "")

            self.uv = member.get("uv", [])
            self.uv_str = ", ".join(self.uv)

            self.room = member["roomNumber"][0] if member["roomNumber"][0] != "NC" else ""
            self.phone = member["telephoneNumber"][0] if member["telephoneNumber"][0] != "NC" else ""
            self.mail = member["mail"][0]

            self.is_student = "student" in member["employeeType"] or "epf" in member["employeeType"] or "student" in \
                              member["eduPersonAffiliation"] or "NC" not in member["formation"]
            self.is_teacher = "faculty" in member["eduPersonAffiliation"] or "researcher" in member["eduPersonAffiliation"]
            self.is_staff = "employee" in member["eduPersonAffiliation"]

            self.title = member["title"][0] if member["title"][0] != "NC" else ""

            self.formation = member["formation"][0] if member["formation"][0] != "NC" else ""
            self.branch = member["filiere"][0] if member["filiere"][0] != "NC" else ""
            self.level = member["niveau"][0] if member["niveau"][0] != "NC" else ""

            self.assignment = member["supannAffectation"][0] if member["supannAffectation"][0] != "NC" else ""
