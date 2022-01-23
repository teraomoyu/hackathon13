$(function() {
    $('#thumb_frame').on('input', function() {
      $('#current_thumb_frame').text($('#thumb_frame').val());
    });
  
    $('#thumb_frame').change(function() {
      $('#current_thumb_frame').text($('#thumb_frame').val());
  
      var image_dir = $('#thumb').attr('src').split('/');
      image_dir.pop();
      $('#thumb').attr('src', image_dir.join('/') + '/' + $('#thumb_frame').val());
    });
  });