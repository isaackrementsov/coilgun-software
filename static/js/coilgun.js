let targetDistance = 0.123;
let max_difference = 0.02;

init();

function init(){
    $('#target-distance').text(targetDistance + 'm');
}

function getPredictedDistance(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, onSuccess){
    $.ajax({
        url: '/distance',
        data: {
            'projectile_area': projectileArea,
            'projectile_mass': projectileMass,
            'fluid_density': fluidDensity,
            'drag_constant': dragConstant,
            'initial_velocity': initialVelocity
        },
        dataType: 'json',
        type: 'get',
        success: function(response){
            onSuccess(response);
        }
    });
}

$('#get-distance').on('click', function(){
    let projectileArea = $('#projectile-area').val();
    let projectileMass = $('#projectile-mass').val();
    let fluidDensity = $('#fluid-density').val();
    let dragConstant = $('#drag-constant').val();
    let initialVelocity = $('#initial-velocity').val();

    getPredictedDistance(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, function(distance){
        $('#predicted-distance').text(Math.round(distance*1000)/1000 + 'm');

        let evaluation = 'Ready to launch';
        let color = '#00E676';
        let difference = distance - targetDistance;

        if(difference < -max_difference){
            evaluation = 'Move the target closer';
            color = '#FF1744';
        }

        if(difference > max_difference){
            evaluation = 'The target is too close';
            color = '#FF1744';
        }

        $('#distance-evaluation').text(evaluation);

        $('#distance-container').animate({'backgroundColor': color});
    });
});
