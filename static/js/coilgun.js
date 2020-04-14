let targetDistance = 0;
let predictedDistance = -1;
let max_difference = 0.10;
let triggerDisabled = true;

$(document).ready(function(){
    init();
    evalTrigger();

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

function evalTrigger(){
    trigger = $('#trigger');

    if(triggerDisabled){
        if(!trigger.hasClass('inactive')) trigger.addClass('inactive');
    }else{
        if(trigger.hasClass('inactive')) trigger.removeClass('inactive');
    }
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

function saveProjectileData(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, name, onSuccess){
    const data =  {
        'projectile_area': projectileArea,
        'projectile_mass': projectileMass,
        'fluid_density': fluidDensity,
        'drag_constant': dragConstant,
        'initial_velocity': initialVelocity,
        'name': name
    };

    $.ajax({
        url: '/save-data',
        data: data,
        type: 'post',
        dataType: 'json',
        success: function(response){
            onSuccess(data, response);
        }
    });
}

$('#get-distance').on('click', function(){
    let projectileArea = $('#projectile-area').val();
    let projectileMass = $('#projectile-mass').val();
    let fluidDensity = $('#fluid-density').val();
    let dragConstant = $('#drag-constant').val();
    let initialVelocity = $('#initial-velocity').val();

    getPredictedDistance(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, distance => {
        predictedDistance = distance;
        $('#predicted-distance').text(predictedDistance.toFixed(3) + 'm');
        evalDistance();
    });
});

$('#save-data').on('click', function(){
    $('#name').toggle(200);
    $(this).toggleClass('cta');
});

$('#submit').on('click', function(){
    let name = $('#name-input').val();
    let projectileArea = $('#projectile-area').val();
    let projectileMass = $('#projectile-mass').val();
    let fluidDensity = $('#fluid-density').val();
    let dragConstant = $('#drag-constant').val();
    let initialVelocity = $('#initial-velocity').val();

    saveProjectileData(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, name, (data, response) => {
        $('#name').toggle(200);
        $(this).toggleClass('cta');

        if(response.id){
            $('#profile-select').append(`
                <option value="projectile-${response.id}">${data.name}</option>
            `);

            $('#hidden-data').append(`
                <div id="projectile-${response.id}">
                    <input type="hidden" class="projectile-area" value="${data.projectile_area}">
                    <input type="hidden" class="projectile-mass" value="${data.projectile_mass}">
                    <input type="hidden" class="fluid-density" value="${data.fluid_density}">
                    <input type="hidden" class="drag-constant" value="${data.drag_constant}">
                    <input type="hidden" class="initial-velocity" value="${data.initial_velocity}">
                    <input type="hidden" class="name" value="${data.name}">
                </div>
            `);

            $(`#profile-select option[value="projectile-${response.id}"]`).attr('selected', 'selected');
        }
    });
});

function evalDistance(){
    if(predictedDistance > 0){
        let evaluation = 'Ready to launch';
        let color = '#00E676';
        let difference = predictedDistance - targetDistance;

        triggerDisabled = false;

        if(difference < -max_difference){
            triggerDisabled = true;
            evaluation = 'Move the target closer';
            color = '#EF5350';
        }

        if(difference > max_difference){
            triggerDisabled = true;
            evaluation = 'The target is too close';
            color = '#EF5350';
        }

        evalTrigger();

        $('#distance-evaluation').text(evaluation);
        $('#distance-container').animate({'backgroundColor': color}, 10);
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

$('#profile-select').on('input', function(){
    let projectileId = $(this).val();
    let projectileInfo = $('#' + projectileId);

    $('#projectile-area').val(projectileInfo.find('.projectile-area').val());
    $('#projectile-mass').val(projectileInfo.find('.projectile-mass').val());
    $('#fluid-density').val(projectileInfo.find('.fluid-density').val());
    $('#drag-constant').val(projectileInfo.find('.drag-constant').val());
    $('#initial-velocity').val(projectileInfo.find('.initial-velocity').val());
    $('#name-input').val(projectileInfo.find('.name').val());
});
