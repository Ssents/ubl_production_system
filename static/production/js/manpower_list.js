var operator ="";
var machine_id = "";
var day = "";
var month = "";
var helpers = "";
var shift = "";


$(".plan-table tbody").on('click', '.editPlan', function(){
    row_id = $(this).closest('tr').attr('id');
    $("#editManpowerPlanForm  #inputPlanId").val(row_id);
    machine_id = $(this).closest('tr').find('.machineId').text();
    $('#editManpowerPlanForm #inputMachineEdit').val(machine_id);
    shift = $(this).closest('tr').find('.shift').text();
    $('#editManpowerPlanForm #inputShiftEdit').val(shift);
    operator = $(this).closest('tr').find('.operator').text();
    $('#editManpowerPlanForm #inputOperatorEdit').val(operator);
    helpers = $(this).closest('tr').find('.helpers').text();
    $('#editManpowerPlanForm #inputHelpersEdit').val(helpers)
   
});


$(".plan-table tbody").on('click', '.deletePlan', function(){
    row_id = $(this).closest('tr').attr('id');
    $("#deleteManpowerPlanForm  #inputPlanIdDelete").val(row_id);
    
});