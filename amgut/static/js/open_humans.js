/*globals $:true, userData:true, accessToken: true, OPEN_HUMANS_URL:true*/

'use strict';

var BARCODE_URL = OPEN_HUMANS_URL + '/american-gut/barcodes/';

$(function () {
  if (!accessToken) {
    return;
  }

  $('.link-barcode').click(function (e) {
    e.preventDefault();

    var barcode = $(this).data('barcode');
    var url = BARCODE_URL + '?access_token=' + accessToken;

    $.post(url, {value: barcode})
      .always(function (result) {
        location.reload();
      });
  });

  $('.unlink-barcode').click(function (e) {
    e.preventDefault();

    var barcode = $(this).data('barcode');
    var url = BARCODE_URL + barcode + '/?access_token=' + accessToken;

    $.ajax(url, {type: 'DELETE'})
      .always(function(result) {
        location.reload();
      });
  });
});
