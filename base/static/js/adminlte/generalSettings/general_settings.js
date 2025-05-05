function convertToJsonForGeneralSetting(selectedSettingId){
    var generalSettingsJsonData = {};
    if(selectedSettingId == 'districtRadio'){
       generalSettingsJsonData.setupType = 'district';
       generalSettingsJsonData.provinceId = $("#province").attr('data-id')?$('#province').attr('data-id'):$('#province').val();
    }
    else if(selectedSettingId == 'provinceRadio'){
     generalSettingsJsonData.setupType = 'province';
     
    }
    else {
     generalSettingsJsonData.setupType = 'vdcMunicipality';
     generalSettingsJsonData.districtId = $("#district").attr('data-id')?$('#district').attr('data-id'):$('#district').val();
    }

    generalSettingsJsonData.name = $("generalSettingName").val();
    generalSettingsJsonData.alias = $("generalSettingAlias").val();

    return JSON.stringify(generalSettingsJsonData);

}