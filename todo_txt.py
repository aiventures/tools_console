""" Todo.txt Object representation """

# import pprint
# import traceback
import re
import hashlib
from datetime import datetime as DateTime
from tools_console import console_utils as cu

class Todo():
    """ class representation of a single todo line item
        https://github.com/todotxt/todo.txt
        #TODO add logger
    """

    # name constants
    ORIGINAL="ORIGINAL"
    DESCRIPTION="DESCRIPTION"
    COMPLETE="IS_COMPLETE"
    DATES="DATES"
    PRIO="PRIO"
    CONTEXTS="CONTEXTS"
    PROJECTS="PROJECTS"
    ATTRIBUTES="ATTRIBUTES"
    LINKS="LINKS"
    LINKS1="LINKS1"
    LINKS2="LINKS2"
    DATE_COMPLETED="DATE_COMPLETED"
    DATE_CREATED="DATE_CREATED"
    DATE_CHANGED="DATE_CHANGED"
    INDEX="INDEX"
    HASH="HASH"
    DEFAULT_COLOR="DEFAULT_COLOR"
    # regex rules to parse a todo line
    TODO_RULES={
        COMPLETE:"^x",
        DATES:r"\d{4}-\d{1,2}-\d{1,2}",
        PRIO:"\([(a-z0-9)]\)",
        CONTEXTS:"@[a-z0-9]+",
        PROJECTS:"\+[a-z0-9]+",
        ATTRIBUTES:"[a-z0-9_-]+:[a-z0-9_-]+",
        LINKS1:r"[^\"^']http+[^\s]+[\w]", #links without quotes
        LINKS2:"[\"']http.+[\"']" #links with quotes
    }

    RULE_LIST=list(TODO_RULES.keys())

    # ALL ATTRIBUTES
    TODO_ATTRIBUTES=[COMPLETE,PRIO,DATE_COMPLETED,DATE_CREATED,DESCRIPTION,LINKS,PROJECTS,CONTEXTS,ATTRIBUTES,DATE_CHANGED,HASH,ORIGINAL]

    # EXCLUDE FROM OUTPUT
    TODO_NO_OUTPUT=[ORIGINAL]

    # color coding for console output
    # color some fields depending on priority / completion
    TODO_COLORS={
        DEFAULT_COLOR:cu.COLOR_DEFAULT,
        COMPLETE:cu.COLOR_GREEN,
        PRIO:cu.COLOR_PURPLE,
        DATE_COMPLETED:cu.COLOR_GREEN,
        DATE_CREATED:cu.COLOR_LIGHTBLUE,
        DESCRIPTION:cu.COLOR_DEFAULT,
        LINKS:cu.COLOR_LIGHTBLUE,
        PROJECTS:cu.COLOR_PURPLE,
        CONTEXTS:cu.COLOR_YELLOW,
        ATTRIBUTES:cu.COLOR_YELLOW,
        DATE_CHANGED:cu.COLOR_YELLOW,
        HASH:cu.COLOR_LIGHTBLUE,
        ORIGINAL:cu.COLOR_GREY
    }

    # white background
    TODO_COLORS_WH={
        DEFAULT_COLOR:cu.COLOR_DEFAULT_WH,
        COMPLETE:cu.COLOR_GREEN_WH,
        PRIO:cu.COLOR_PURPLE_WH,
        DATE_COMPLETED:cu.COLOR_GREEN_WH,
        DATE_CREATED:cu.COLOR_LIGHTBLUE_WH,
        DESCRIPTION:cu.COLOR_DEFAULT_WH,
        LINKS:cu.COLOR_LIGHTBLUE_WH,
        PROJECTS:cu.COLOR_PURPLE_WH,
        CONTEXTS:cu.COLOR_YELLOW_WH,
        ATTRIBUTES:cu.COLOR_YELLOW_WH,
        DATE_CHANGED:cu.COLOR_YELLOW_WH,
        HASH:cu.COLOR_LIGHTBLUE_WH,
        ORIGINAL:cu.COLOR_GREY_WH
    }

    # colored background
    TODO_COLORS_BG={
        DEFAULT_COLOR:cu.COLOR_DEFAULT_BG,
        COMPLETE:cu.COLOR_GREEN_BG,
        PRIO:cu.COLOR_PURPLE_BG,
        DATE_COMPLETED:cu.COLOR_GREEN_BG,
        DATE_CREATED:cu.COLOR_LIGHTBLUE_BG,
        DESCRIPTION:cu.COLOR_DEFAULT_BG,
        LINKS:cu.COLOR_LIGHTBLUE_BG,
        PROJECTS:cu.COLOR_PURPLE_BG,
        CONTEXTS:cu.COLOR_YELLOW_BG,
        ATTRIBUTES:cu.COLOR_YELLOW_BG,
        DATE_CHANGED:cu.COLOR_YELLOW_BG,
        HASH:cu.COLOR_LIGHTBLUE_BG,
        ORIGINAL:cu.COLOR_DEFAULT_BG
    }    

    colormap = TODO_COLORS.copy()

    def __init__(self,*args) -> None:
        """ Constructor:
            receives attributes as dict (just with get_todo_dict)
        """
        if not args or (len(args)>0 and not isinstance(args[0],dict)):
            return
        att_dict=args[0]
        keys = [k for k in list(att_dict.keys()) if k.upper() in Todo.TODO_ATTRIBUTES]
        for k in keys:
            setattr(self,k.lower(),att_dict[k])

    def get_attributes(self)->dict:
        """ gets todo attributes as dict """
        out={}
        for t in Todo.TODO_ATTRIBUTES:
            try:
                out[t]=getattr(self,t.lower())
            except AttributeError:
                continue
        return out

    def colorize(self,color_map=None):
        """ Returns colored todo line
            color_dict (dict): color map (Todo.TODO_COLORS if no parameter set)
        """
        if not color_map:
            color_map=Todo.TODO_COLORS
        todo_dict=self.get_attributes()
        return Todo.get_todo_string(todo_dict,color_map=color_map)

    def __str__(self):
        """ Gets object as Todo.txt string"""
        return Todo.get_todo_string(self.get_attributes())

    def __repr__(self):
        """ Gets object as Todo.txt string"""
        return repr(self.get_attributes())

    @staticmethod
    def get_todo_dict(todo:str)->dict:
        """ transforms a todo line into a dict according to todo.txt spec """

        todo_dict={}
        todo_dict[Todo.HASH]=hashlib.md5(todo.encode()).hexdigest()
        todo_dict[Todo.ORIGINAL]=todo
        description = todo
        # print(f"--- TASK {task}")
        for rule,regex in Todo.TODO_RULES.items():
            re_finds=re.findall(regex,todo,re.IGNORECASE)
            if re_finds:
                for re_find in re_finds:
                    description = description.replace(re_find,"",1)
                # remove any duplicates
                re_finds=list(dict.fromkeys(re_finds))
                todo_dict[rule]=re_finds
                # print(f"    RULE {rule:<15}: {re_finds}")

        # description is what is left over
        description=" ".join([s for s in description.split(" ") if s != ''])

        todo_dict[Todo.DESCRIPTION]=description
        # print(f"    DESCRIPTION         : {description}")

        # clean up data / special cases
        todo_keys = list(todo_dict.keys())

        # post process links
        links=[]
        if Todo.LINKS1 in todo_keys:
            links.extend(todo_dict.pop(Todo.LINKS1))
        if Todo.LINKS2 in todo_keys:
            links.extend(todo_dict.pop(Todo.LINKS2))
        links=[l.strip().replace('"',"") for l in links]
        links=[l.strip().replace("'","") for l in links]
        if links:
            todo_dict[Todo.LINKS]=links

        # completion
        todo_dict[Todo.COMPLETE] = True if Todo.COMPLETE in todo_keys else False

        # check for attributes
        if Todo.ATTRIBUTES in todo_keys:
            attributes = {att.split(":",1)[0]:att.split(":",1)[1] for att in todo_dict[Todo.ATTRIBUTES]}
            # convert values
            for k,v in attributes.items():
                if k.lower().startswith("date"):
                    try:
                        attributes[k]=DateTime.strptime(v,"%Y-%m-%d")
                    except ValueError:
                        pass

            todo_dict[Todo.ATTRIBUTES]=attributes


        # check for multiple priorities, only pick the first
        if Todo.PRIO in todo_keys:
            todo_dict[Todo.PRIO]=todo_dict[Todo.PRIO][0][1].upper()

        # check for dates - logic being used
        # for two dates: completion data + start date > set completion flag
        # for one date:  completion date if completed, start date otherwise
        if Todo.DATES in todo_keys:
            dates = todo_dict[Todo.DATES]
            dates = [DateTime.strptime(d,'%Y-%m-%d') for d in dates]
            if len(dates)>=2:
                todo_dict[Todo.COMPLETE] = True
                todo_dict[Todo.DATE_COMPLETED]=dates[0]
                todo_dict[Todo.DATE_CREATED]=dates[1]
            elif len(dates)==1:
                if todo_dict[Todo.COMPLETE]:
                    todo_dict[Todo.DATE_COMPLETED] = dates[0]
                else:
                    todo_dict[Todo.DATE_CREATED] = dates[0]

        return todo_dict

    @staticmethod
    def get_todo_string(todo_dict,changed=False,color_map=None):
        """ Creates Todo String from Todo Dict
            changed: sets change flag
            color_map: color output
        """

        def colorize(v,att:str)->str:
            if not color_map:
                return v

            color = color_map.get(att,color_map[Todo.DEFAULT_COLOR])
            out = v

            if isinstance(v,str):
                out = cu.get_col_text(v,color)
            elif isinstance(v,list):
                out = [cu.get_col_text(li,color) for li in v]
            return out

        todo=[]
        for att in Todo.TODO_ATTRIBUTES:
            v = todo_dict.get(att)
            # print(f"{att} => {v}")
            items=[]
            s = None
            if v:
                if isinstance(v,list):
                    v = sorted(v,key=str.casefold)
                if att == Todo.COMPLETE:
                    s = "X"
                elif att == Todo.PRIO:
                    s = "("+v+")"
                elif "DATE" in att and isinstance(v,DateTime):
                    s = v.strftime("%Y-%m-%d")
                elif att == Todo.DESCRIPTION:
                    s = v
                elif att == Todo.LINKS:
                    items = ['"'+li+'"' for li in v]
                    s = " ".join(items)
                elif att == Todo.PROJECTS or att == Todo.CONTEXTS:
                    s = " ".join(v)
                elif att == Todo.ATTRIBUTES:
                    for k,p in v.items():
                        if changed and k.lower()==Todo.DATE_CHANGED.lower():
                            continue
                        if isinstance(p,DateTime):
                            p=p.strftime("%Y-%m-%d")
                        items.append(str(k)+":"+str(p))
                    s = " ".join(items)
                elif att == Todo.ORIGINAL:
                    pass
                elif att == Todo.HASH:
                    s = "@hash:"+str(v)

                if s:
                    todo.append(colorize(s,att))

        # add date change
        if changed and todo:
            v=Todo.DATE_CHANGED.lower()+":"+DateTime.now().strftime("%Y-%m-%d")
            todo.append(colorize(v,att))

        return " ".join(todo)
