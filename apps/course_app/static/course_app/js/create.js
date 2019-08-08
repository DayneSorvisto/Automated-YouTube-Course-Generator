/* eslint-disable prefer-arrow-callback */
/* eslint-disable func-names */

$(document).ready(function () {
  console.log('load');
  $('.add-subject').hide();
  $('.add-category').hide();

  $('#subject_id').on('change', function () {
    // console.log('sub change');
    if ($(this).val() === 'add') {
      // console.log('new subject');
      $('.add-subject').show();
    }
    else {
      $('.add-subject').hide();
    }
  });

  $('#category_id').on('change', function () {
    if ($(this).val() === 'add') {
      $('.add-category').show();
    }
    else {
      $('.add-category').hide();
    }
  });

});
