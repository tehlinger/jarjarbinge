#Remove object id
%s/'_id': ObjectId('.*'),//g

#Replace ' with "
%s/'/"/g

#Remove the first surrounding quoes in lists
%s/: \["{"/: \[{"/g
%s/}"\], "/}\], "/g

#Remove None
%s/None/""/g

####From mongoexport code####

%s/ "_id" : { "$oid" : ".*" },//g
%s/\\//g 
%s/null/""
