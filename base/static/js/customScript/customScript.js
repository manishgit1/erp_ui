

function loadSelectElementData(selectElementId, requestUrl, jsonKey, jsonValue){
   $('#'+ selectElementId).select2();

   var jsonData = {
      "setupType": jsonValue
   };


   debugger

   $.ajax({
    "url": requestUrl + "?jsonData="+ encodeURI(JSON.stringify(jsonData)),
    "method": "GET",
    "dataType": "json",
    success: function(data){
         if(data.hasOwnProperty('resultCode')){
          if(!data.resultCode === '0'){
              
          }
          else {
           console.log(data);
          }
         }
    },
    error: function(error){
     console.error(error);
    }
   })


}



// function loadDistrictProvinceByMunicipality(id){
      
//    $.ajax({
//       "url": ""
//    })
// }
