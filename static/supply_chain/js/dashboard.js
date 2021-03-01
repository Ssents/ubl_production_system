// EDIT FORM FILLING
var row_id = "";
var coil_number = "";
var coil_gauge = 0;
var coil_width = 0;
var coil_finish = "";
var coil_colour = "";
var initial_mass = 0;
var final_mass = 0;

$("table tbody").on('click', '.coilNumbertd',function(){
    coil_id = $(this).closest('tr').attr('id');
    var coil = getCoilValues(coil_id);
    console.log(coil.coil_number,coil.coil_gauge, coil.coil_width, coil.coil_colour, 
                coil.coil_finish,'initial mass',coil.initial_mass, coil.initial_running_meters);
    
    $("#editCoilForm #coilNumber").val(coil.coil_number);
    $("#editCoilForm #initialMass").val(coil.initial_mass);
    $("#editCoilForm #inputRunningMeters").val(coil.initial_running_meters);
    $("#editCoilForm #gaugeValdation").val(coil.coil_gauge);
    $("#editCoilForm #widthValdation").val(coil.coil_width);
    $("#editCoilForm #colourValdation").val(coil.coil_colour);
    $("#editCoilForm #finishValdation").val(coil.coil_finish);
    $("#editCoilForm #coilId").val(coil_id);
    // $("#editCoilForm #initialMass").val(coil.initial_mass);



});



$("table tbody").on('click', '.deleteCoilButton',function(){
    coil_id = $(this).closest('tr').attr('id');
    var coil = getCoilValues(coil_id);

    $("#deleteCoilForm #coilIdDelete").val(coil_id);
    $("#deleteCoilForm #coilNumberDelete").text(coil.coil_number);
    console.log(coil_id);
});



$("table tbody").on('click', '.tranferMaterial',function(){
    coil_id = $(this).closest('tr').attr('id');
    var coil = getCoilValues(coil_id);

    $("#transferCoilForm #coilIdTransfer").val(coil_id);
    $("#transferCoilForm #coilNumberTransfer").text(coil.coil_number);
    console.log(coil_id);
});

function getCoilValues(row_id){
    coil_number = $("#"+row_id).find(".coilNumberSpan").html();
    coil_gauge = $("#"+row_id).find(".coilGauge").html();
    coil_width = $("#"+row_id).find(".coilWidth").html();
    coil_colour = $("#"+row_id).find(".coilColour").html();
    coil_finish = $("#"+row_id).find(".coilFinish").html();
    initial_mass = $("#"+row_id).find(".initialMass").html();
    initial_running_meters = $("#"+row_id).find(".initialRunningMeters").html();
    final_mass = $("#"+row_id).find(".finalMass").html();

    return {
        'coil_number':coil_number,
        'coil_gauge':coil_gauge,
        'coil_width': coil_width,
        'coil_colour': coil_colour,
        'coil_finish': coil_finish,
        'initial_mass': initial_mass,
        'final_mass':final_mass,
        'coil_id': row_id,
        'initial_running_meters':initial_running_meters
    };

}