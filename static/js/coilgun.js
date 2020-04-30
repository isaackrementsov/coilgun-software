// Isaac Krementsov
// 4/5/2020
// Introduction to Systems Engineering
// Coilgun Software (frontend)- User interface for working with coilgun projectile launcher


// Global variables

// Will store the distance of the coilgun's target, sensed by the UDS
let targetDistance = 0;

// Will store the distance the server predicts the projectile will travel
let predictedDistance = -1;

// Maximum allowed difference between predicted and target distances
let maxDifference = 0.10;

// Whether or not the trigger is disabled (|targetDistance - predictedDistance| < maxDifference)
let triggerDisabled = true;


// Wait for the DOM to load before operating on it
$(document).ready(function(){
    // Preform all actions necessary to prepare the user interface
    init();
    // Disable the trigger
    evalTrigger();

    // Generate a WebSocket connection with the server (uses localhost:5000 automatically)
    const socket = io();

    // Wait for the server to respond with a connected status
    socket.on('connect', () => {

        // Respond each time the server sends UDS data
        socket.on('data', msg => {
            // Get the UDS data and display it in the UI
            targetDistance = msg.reading.toFixed(3);
            $('#target-distance').text(targetDistance + 'm');

            // Check the difference between this target distance and the predicted distance
            evalDistance();
        });

    });

});


// Update the target distance with an initial value
function init(){
    $('#target-distance').text(targetDistance + 'm');
}


// Decide whether the trigger can be enabled and update UI accordingly
function evalTrigger(){
    // <button id="trigger">...</button>
    trigger = $('#trigger');

    if(triggerDisabled){
        // If the trigger is newly disabled, update its appearance with the inactive class
        if(!trigger.hasClass('inactive')) trigger.addClass('inactive');
    }else{
        // If the trigger is newly enabled, update its appearance by removing the inactive class
        if(trigger.hasClass('inactive')) trigger.removeClass('inactive');
    }
}


// Contact the server and get the predicted projectile travel distance
function getPredictedDistance(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, onSuccess){
    // Send an AJAX GET request to '/distance'
    $.ajax({
        url: '/distance',
        // Send user submitted form data
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
            // Apply the onSuccess callback passed into this function to the response data
            onSuccess(response);
        }
    });
}


// Send projectile data to the server to be saved
function saveProjectileData(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, name, onSuccess){
    const data =  {
        'projectile_area': projectileArea,
        'projectile_mass': projectileMass,
        'fluid_density': fluidDensity,
        'drag_constant': dragConstant,
        'initial_velocity': initialVelocity,
        'name': name
    };

    // Send an AJAX POST request to '/save-data'
    $.ajax({
        url: '/save-data',
        data: data,
        type: 'post',
        dataType: 'json',
        success: function(response){
            // Handle response data with the onSuccess callback
            onSuccess(data, response);
        }
    });
}


// Get predicted distance for user in response to button click
$('#get-distance').on('click', function(){
    // Get input values
    let projectileArea = $('#projectile-area').val();
    let projectileMass = $('#projectile-mass').val();
    let fluidDensity = $('#fluid-density').val();
    let dragConstant = $('#drag-constant').val();
    let initialVelocity = $('#initial-velocity').val();

    // Contact the server to get the distance response
    getPredictedDistance(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, distance => {
        // Update the global predicted distance
        predictedDistance = distance;
        // Show the new distance in the user interface
        $('#predicted-distance').text(predictedDistance.toFixed(3) + 'm');

        // Evaluate the difference between the new predicted and existing target distances
        evalDistance();
    });
});


// Open the projectile data save menu
$('#save-data').on('click', function(){
    // Show the profile name input / submit button container and grey out this button
    $('#name').toggle(200);
    $(this).toggleClass('cta');
});

// Save projectile data for the user
$('#submit').on('click', function(){
    // Get the input values
    let name = $('#name-input').val();
    let projectileArea = $('#projectile-area').val();
    let projectileMass = $('#projectile-mass').val();
    let fluidDensity = $('#fluid-density').val();
    let dragConstant = $('#drag-constant').val();
    let initialVelocity = $('#initial-velocity').val();

    // Send the data to the server to be saved
    saveProjectileData(projectileArea, projectileMass, fluidDensity, dragConstant, initialVelocity, name, (data, response) => {
        // Hide the save menu again
        $('#name').toggle(200);
        // Grey out the submit button
        $(this).toggleClass('cta');

        // The id of the newly saved profile should be sent back if it was saved successfully
        if(response.id){
            // Add an option to select the newly saved profile again
            $('#profile-select').append(`
                <option value="projectile-${response.id}">${data.name}</option>
            `);

            // Add the hidden data so it will be loaded if this profile is selected again
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

            // Make the new profile currently selected
            $(`#profile-select option[value="projectile-${response.id}"]`).attr('selected', 'selected');
        }
    });
});


// Compare the predicted and target distances
function evalDistance(){
    // Make sure predicted distance is postive (meaning it has been recorded from the server)
    if(predictedDistance > 0){
        // Initially assume the projectile is ready to launch
        let evaluation = 'Ready to launch';
        let color = '#00E676';
        triggerDisabled = false;

        // Find the difference between predicted and target distances
        let difference = predictedDistance - targetDistance;

        // If the difference is too negative, the target distance is too high
        if(difference < -maxDifference){
            // Disable the trigger
            triggerDisabled = true;
            // Tell the user to move the target
            evaluation = 'Move the target closer';
            // Use a red color to signify an error
            color = '#EF5350';
        }

        // If the difference is too positive, the target distance is too low
        if(difference > maxDifference){
            // Distable the trigger
            triggerDisabled = true;
            // Tell the user to move the target away
            evaluation = 'The target is too close';
            // Use a red color to signify an error
            color = '#EF5350';
        }

        // Update the trigger button according to the distance evaluation
        evalTrigger();

        // Use color coding and display text to notify the user of the distance status
        $('#distance-evaluation').text(evaluation);
        $('#distance-container').animate({'backgroundColor': color}, 10);
    }
}


// Show info boxes for the form symbols
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


// Show saved profiles when they are selected by the user
$('#profile-select').on('input', function(){
    // Get the projectile id to be selected
    let projectileId = $(this).val();
    // Get the hidden input container for this projectile
    let projectileInfo = $('#' + projectileId);

    // Populate the forms with the saved data, allowing the user to get a distance or update the record
    $('#projectile-area').val(projectileInfo.find('.projectile-area').val());
    $('#projectile-mass').val(projectileInfo.find('.projectile-mass').val());
    $('#fluid-density').val(projectileInfo.find('.fluid-density').val());
    $('#drag-constant').val(projectileInfo.find('.drag-constant').val());
    $('#initial-velocity').val(projectileInfo.find('.initial-velocity').val());
    $('#name-input').val(projectileInfo.find('.name').val());
});
