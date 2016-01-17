$(document).ready(function() {
    $('#sel').on('change', function() {
        if ($('#sel').val() == 'chronos') {
            $('#chronos').css('display', 'block');
            $('#marathon').css('display', 'none');
        } else {
            $('#marathon').css('display', 'block');
            $('#chronos').css('display', 'none');
        }
    });
});