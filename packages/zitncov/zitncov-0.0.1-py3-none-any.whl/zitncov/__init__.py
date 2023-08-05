# The platfrom url
host = "https://api.zit.edu.cn"
purl = "https://lightapp.zit.edu.cn"
endpoints = {
        "login":host+"/login",
        "oauthorize":host+"/oauth/authorize",
        "sign":purl+"/api/questionnaire/questionnaire/addMyAnswer"
}
params={
    "client_id":"pqZ3wGM07i8R9mR3",
    "redirect_uri":"https://lightapp.zit.edu.cn/check/questionnaire",
    "response_type":"code",
    "scope":"base_api",
    "state":"ruijie"
}
authorityid=f'["10025","10081","10214","10263"]'