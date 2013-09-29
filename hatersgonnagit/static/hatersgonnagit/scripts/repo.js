/* globals jQuery, haters */
'use strict';

(function ($, document, undefined) {
  var progressbar = $('#elements-progress');

  function progress(increment) {
    var value = parseInt(progressbar.attr('aria-valuenow'), 10);
    value += increment;
    progressbar.attr('aria-valuenow', value);
    progressbar.attr('aria-valuenow', value);
    progressbar.attr('style', 'width: ' + value + '%;');
    progressbar.find('.sr-only').html(value + '%;');
    if (value === 100) {
      $('#loading h1').html('Passing Haters Test...');
    }
  }

  function init() {
    $.each(haters.urls, function (key) {
      $.ajax({
        'url': this
      }).success(function (data) {
        console.log(data);
        progress(30);
        $('#element-progress').html(key);
      });
    });
  }

  $(document).ready(init);

})(jQuery, document);
