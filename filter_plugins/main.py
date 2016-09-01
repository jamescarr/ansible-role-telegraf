import re
import datetime


def dumps(o):
    """Returns a string containing the toml corresponding to o, a dictionary"""
    retval = ""
    addtoretval, sections = _dump_sections(o, "")
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = _dump_sections(sections[section], section)
            if addtoretval:
                retval += "["+section+"]\n"
                retval += addtoretval
            for s in addtosections:
                newsections[section+"."+s] = addtosections[s]
        sections = newsections
    return retval

def _dump_sections(o, sup):
    retstr = ""
    if sup != "" and sup[-1] != ".":
        sup += '.'
    retdict = {}
    arraystr = ""
    for section in o:
        qsection = section
        if not re.match(r'^[A-Za-z0-9_-]+$', section):
            if '"' in section:
                qsection = "'" + section + "'"
            else:
                qsection = '"' + section + '"'
        if not isinstance(o[section], dict):
            arrayoftables = False
            if isinstance(o[section], list):
                for a in o[section]:
                    if isinstance(a, dict):
                        arrayoftables = True
            if arrayoftables:
                for a in o[section]:
                    arraytabstr = ""
                    arraystr += "[["+sup+qsection+"]]\n"
                    s, d = _dump_sections(a, sup+qsection)
                    if s:
                        if s[0] == "[":
                            arraytabstr += s
                        else:
                            arraystr += s
                    while d != {}:
                        newd = {}
                        for dsec in d:
                            s1, d1 = _dump_sections(d[dsec], sup+qsection+"."+dsec)
                            if s1:
                                arraytabstr += "["+sup+qsection+"."+dsec+"]\n"
                                arraytabstr += s1
                            for s1 in d1:
                                newd[dsec+"."+s1] = d1[s1]
                        d = newd
                    arraystr += arraytabstr
            else:
                if o[section] is not None:
                    retstr += (qsection + " = " +
                               str(_dump_value(o[section])) + '\n')
        else:
            retdict[qsection] = o[section]
    retstr += arraystr
    return (retstr, retdict)

def _dump_value(v):
    if isinstance(v, list):
        t = []
        retval = "["
        for u in v:
            t.append(_dump_value(u))
        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)
                else:
                    retval += " " + str(u) + ","
            t = s
        retval += "]"
        return retval
    if isinstance(v, (str, unicode)):
        v = "%r" % v
        if v[0] == 'u':
            v = v[1:]
        singlequote = v[0] == "'"
        v = v[1:-1]
        if singlequote:
            v = v.replace("\\'", "'")
            v = v.replace('"', '\\"')
        v = v.replace("\\x", "\\u00")
        return str('"'+v+'"')
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, datetime.datetime):
        return v.isoformat()[:19]+'Z'
    if isinstance(v, float):
        return str(v)
    return v


class FilterModule(object):
    def filters(self):
        return {'to_toml': dumps}
