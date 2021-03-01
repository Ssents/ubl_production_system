// get date
currentDate = new Date();
const day = currentDate.getDate();
const month = currentDate.getMonth() + 1;
const year = currentDate.getFullYear();

date_today = `${day}/${month}/${year}`;
console.log(date_today);

document.getElementById('currentDate').innerHTML = date_today;

// lets get the values

var gauge = "";
var width = "";
var colour = "";
var type = "";
var finish = "";
var row_id = "";

$(".table tbody").on('click', '.createPlan', function(){
    row_id = $(this).closest('tr').attr('id');

    
    gauge = $(this).closest('tr').find('.gauge').text();
    width = $(this).closest('tr').find('.width').text();
    colour = $(this).closest('tr').find('.colour').text();
    finish = $(this).closest('tr').find('.finish').text();
    type = $(this).closest('tr').find('.type').text();

    $('#createPlanForm #inputGauge').val(gauge);
    $('#createPlanForm #inputWidth').val(width);
    $('#createPlanForm #inputColour').val(colour);
    $('#createPlanForm #inputFinish').val(finish);


    // $('#createPlanForm #inputproductionType').val(productionType);


    console.log(row_id, gauge, width, colour, finish);
});

$('#createPlanForm').on('change', '#inputProductionType', function(){
    var productionType = $('#createPlanForm #inputProductionType').val();
    var orderNumberInput = $('#createPlanForm #InputOrderNumber');
    if (productionType == "Standard"){
        $('#createPlanForm #inputOrderNumber').val(type);
    }
    else {
        $('#createPlanForm #inputOrderNumber').val("");
    }
    console.log(productionType, type);
});


$(".plan-table tbody").on('click', '.editPlan', function(){
    row_id = $(this).closest('tr').attr('id');
    console.log(row_id);

    gauge = $(this).closest('tr').find('.gauge').text();
    width = $(this).closest('tr').find('.width').text();
    colour = $(this).closest('tr').find('.colour').text();
    finish = $(this).closest('tr').find('.finish').text();
    type = $(this).closest('tr').find('.type').text();
    let machine_name = $(this).closest('tr').find('.machineName').text();
    let shift = $(this).closest('tr').find('.shift').text();
    let order_number = $(this).closest('tr').find('.orderNumber').text();
    let production_type = $(this).closest('tr').find('.productionType').text();
    let tonage = $(this).closest('tr').find('.tonage').text();
    let plan_id = $(this).closest('tr').attr('id');

    let machine_id = $(this).closest('tr').find('.machineId').text();

    console.log(machine_id);
    
    $('#editPlanForm #inputMachineNameEdit').val(machine_id);
    $('#editPlanForm #inputShiftEdit').val(shift);
    $('#editPlanForm #inputProductionTypeEdit').val(production_type)
    $('#editPlanForm #inputOrderNumberEdit').val(order_number);
    $('#editPlanForm #inputTonageEdit').val(tonage);
    $('#editPlanForm #inputPlanIdEdit').val(plan_id);
});




$(".plan-table tbody").on('click', '.deletePlan', function(){
    row_id = $(this).closest('tr').attr('id');
    $("#deletePlanForm #inputPlanIdDelete").val(row_id);
    
});