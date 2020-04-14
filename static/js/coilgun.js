let targetDistance = 0;
let predictedDistance = -1;
let max_difference = 0.10;

$(document).ready(function(){
    init();

    const socket = io();

    socket.on('connect', () => {

        socket.on('data', msg => {
            targetDistance = msg.reading.toFixed(3);
            $('#target-distance').text(targetDistance + 'm');
            evalDistance();
        });

    });

});

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
        predictedDistance = distance;
        $('#predicted-distance').text(predictedDistance.toFixed(3) + 'm');
        evalDistance();
    });
});

function evalDistance(){
    if(predictedDistance > 0){
        let evaluation = 'Ready to launch';
        let color = '#00E676';
        let difference = predictedDistance - targetDistance;

        if(difference < -max_difference){
            evaluation = 'Move the target closer';
            color = '#FF1744';
        }

        if(difference > max_difference){
            evaluation = 'The target is too close';
            color = '#FF1744';
        }

        $('#distance-evaluation').text(evaluation);

        $('#distance-container').animate({'backgroundColor': color}, 100);
    }
}

$('.form-group label i').on({
    mouseenter: function(){
        let parentId = $(this).parent().parent().attr('id');

        $('#' + parentId + ' .info').show(200);
    },
    mouseleave: function(){
        let parentId = $(this).parent().parent().attr('id');

        $('#' + parentId + ' .info').hide(200);
    }
});
