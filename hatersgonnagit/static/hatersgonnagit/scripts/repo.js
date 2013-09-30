/* globals jQuery, haters */
'use strict';

(function ($, document, undefined) {
  var progressbar;
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

  function descending(a, b) {
    return b - a;
  }

  function calculateHatersScore() {
    var merged = {}, hater, liker,
        positive = {}, positiveKeys = [],
        negative = {}, negativeKeys = [];
    $.each(haters.elements, function () {
      $.each(this, function (username) {
        if (merged[username] === undefined) {
          merged[username] = {};
          merged[username].pos = 0;
          merged[username].neg = 0;
          merged[username].meta = this.meta;
        }
        merged[username].pos += this.pos;
        merged[username].neg += this.neg;
      });
    });
    $.each(merged, function (username) {
      var pos = this.pos,
          neg = this.neg;
      if (positive[pos] === undefined) {
        positive[pos] = [];
        positiveKeys.push(pos);
      }
      positive[pos].push(username);
      if (negative[neg] === undefined) {
        negative[neg] = [];
        negativeKeys.push(neg);
      }
      negative[neg].push(username);
    });
    positiveKeys.sort(descending);
    negativeKeys.sort(descending);
    hater = merged[positive[positiveKeys[0]][0]];
    liker = merged[negative[negativeKeys[0]][0]];
    showHater(hater, liker);
  }

  function showHater(hater, liker) {
    var can, ctx, img, haterImage, avatarImg;
    haters.hater = hater;
    haters.liker = liker;
    haterImage = haters.images[0];  // This can be randomized
    $('#canvas')
      .attr('width', haterImage.width)
      .attr('height', haterImage.height);
    can = document.getElementById('canvas');
    ctx = can.getContext('2d');
    img = new Image();
    img.src = haterImage.src;
    img.onload = function () {
      avatarImg = new Image();
      avatarImg.src = hater.meta.avatar_url;
      avatarImg.onload = function () {
        ctx.drawImage(img, 0, 0);
        ctx.drawImage(avatarImg, haterImage.x, haterImage.y);
      };
    };
    $('#hater')
      .html(hater.meta.login)
      .attr('href', hater.meta.html_url);
    $('#loading').delay(1000).fadeOut(400);
    $('#scores').delay(1400).fadeIn(400);

  }

  function init() {
    progressbar = $('#elements-progress');
    $('#scores').hide();
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
