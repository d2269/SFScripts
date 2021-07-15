String soqlQuery = 'Select ID From Flow Where (Status =  \'Obsolete\' OR Status =  \'Draft\') AND VersionNumber > 1';
String orgUrl = URL.getSalesforceBaseUrl().toExternalForm();
HttpRequest flowIdRequest = new HttpRequest();
flowIdRequest.setMethod('GET');
flowIdRequest.setHeader('Authorization', 'Bearer ' + UserInfo.getSessionId());
flowIdRequest.setEndpoint(orgUrl+'/services/data/v50.0/tooling/query?q=SELECT+id,status+FROM+Flow+Where+(+Status+=+\'Obsolete\'+OR+Status+=+\'Draft\'+)+AND+VersionNumber+>+1');
//flowIdRequest.setTimeout(120000); 
Http http = new Http();
HttpResponse httpResponse = http.send(flowIdRequest);
List<Object> records = (List<Object>)((Map<String, Object>)JSON.deserializeUntyped(httpResponse.getBody())).get('records');

//get id
String[] ids = new List<String>();
for (Object variable : records) {
    String str = variable.ToString();
	String res = str.substringBefore(', Status');
	res = res.substringAfter('Id=');
    ids.add(res);
}
//delete
HttpRequest flowIdRequestDelete = new HttpRequest();
for (String idFlow : ids) {    
	flowIdRequestDelete.setMethod('DELETE');
	flowIdRequestDelete.setHeader('Authorization', 'Bearer ' + UserInfo.getSessionId());
	flowIdRequestDelete.setEndpoint(orgUrl +'/services/data/v50.0/tooling/sobjects/Flow/'+idFlow);
	Http http = new Http();
	HttpResponse httpResponseDelete = http.send(flowIdRequestDelete);
}