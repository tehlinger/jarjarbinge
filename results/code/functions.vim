#Replace ' with "
%s/'/"/g
#Delete '\'
%s/\\//g 
#Remove object id
%s/"_id": ObjectId(".*"),//g
#Remove None
%s/None/""/g

#Remove the first surrounding quoes in lists
%s/: "\["{"/: \[{"/g
%s/}"\]", "/}\], "/g
%s/}"\]" }/}\] }/g

####From mongoexport code####

%s/ "_id" : { "$oid" : ".*" },//g
%s/\\//g 
%s/null/""
