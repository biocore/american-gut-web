/*globals $:true, Cookies:true*/

'use strict';

$(function () {
  if ($('.participant').length === 1) {
    $('.participant').attr('checked', 'checked');
  }

  $('#connect-open-humans').click(function () {
    var participants = $('.participant:checked').map(function () {
      return $(this).data('survey-id');
    }).get();

    Cookies.set('link-survey-id', btoa(JSON.stringify(participants)));
  });
});
