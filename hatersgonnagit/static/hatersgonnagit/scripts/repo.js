/* globals jQuery, haters */
'use strict';

(function ($, document, undefined) {
  var progressbar = $('#elements-progress');
  haters.elements = {};

  function progress(increment) {
    var value = parseInt(progressbar.attr('aria-valuenow'), 10);
    value += increment;
    progressbar.attr('aria-valuenow', value);
    progressbar.attr('aria-valuenow', value);
    progressbar.attr('style', 'width: ' + value + '%;');
    progressbar.find('.sr-only').html(value + '%;');
    if (value === 100) {
      $('#loading h1').delay(5000).html('Passing Haters Test...');
      calculateHatersScore();
    }
  }

  function calculateHatersScore() {
    $('#loading').delay(1000).fadeOut(800);
    $('#scores').delay(1000).fadeIn(800);
  }

  function init() {
    $.each(haters.urls, function (key) {
      var jqxhr = $.ajax({
        'url': this,
        'dataType': 'json',
        'method': 'get'
      });
      jqxhr.done(function (data) {
        haters.elements[key] = data;
        $('#element-progress').html(key);
      });
      jqxhr.always(function () {
        progress(30);
      });
    });
  }

  $(document).ready(init);

})(jQuery, document);
