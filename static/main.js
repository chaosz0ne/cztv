var get_media = function() {
	$.get('get_media', function(res) {
		$('#S1 .filename').text(res.S1);
		$('#S2 .filename').text(res.S2);
		$('#S3 .filename').text(res.S3);
	});
	window.setTimeout(get_media, 2000);
}
window.setTimeout(get_media, 2000);


var curstate = {};
curstate.S1 = {};
curstate.S1.elapsed = null;
curstate.S1.len = null;
curstate.S1.elapsed_start = null;
curstate.S1.pause = '';
curstate.S2 = {};
curstate.S2.elapsed = null;
curstate.S2.len = null;
curstate.S2.elapsed_start = null;
curstate.S2.pause = '';
curstate.S3 = {};
curstate.S3.elapsed = null;
curstate.S3.len = null;
curstate.S3.elapsed_start = null;
curstate.S3.pause = '';



var update_elapsed_one = function(mystate, my_id) {
  if (mystate.pause !== 'enabled' && mystate.elapsed !== null) {
    var to_add = (Date.now() - mystate.elapsed_start) / 1000; 
    $(my_id + ' .remaining').text(formattimestamp(mystate.len - (mystate.elapsed + to_add)));
  }
}

var update_elapsed = function() {
  update_elapsed_one(curstate.S1, '#S1');
  update_elapsed_one(curstate.S2, '#S2');
  update_elapsed_one(curstate.S3, '#S3');
  window.setTimeout(update_elapsed, 100);
}
window.setTimeout(update_elapsed, 100);


var formattimestamp = function(tme) {
   return (tme/60>>0) + ':' + (tme % 60).toFixed(1);
}

var sync_stuff = function(my_res, mystate, my_id) {
    if (my_res !== undefined) {
      $(my_id + ' .length').text(formattimestamp(my_res.length));
      $(my_id + ' .remaining').text(formattimestamp(my_res.length - my_res.elapsed));
      mystate.len = my_res.length;
      mystate.elapsed = my_res.elapsed;
      mystate.pause = my_res.pause;
      remaining = mystate.len - mystate.elapsed;
      if (remaining < 60) {
        $(my_id + '').removeClass('t-5');
        $(my_id + '').addClass('t-1');
      } else if (remaining < (60 * 5)) {
        // 5 minutes left
        $(my_id + '').addClass('t-5');
        $(my_id + '').removeClass('t-1');
      } else {
        $(my_id + '').removeClass('t-5');
        $(my_id + '').removeClass('t-1');
      }
      console.log('Setting elapsed to ' + mystate.elapsed);
      mystate.elapsed_start = Date.now();
    } else {
      $(my_id + ' .length').text("");
      $(my_id + ' .remaining').text("");
      $(my_id + '').removeClass('t-5');
      $(my_id + '').removeClass('t-1');
      mystate.elapsed = null;
      mystate.elapsed_start = null;
      mystate.pause = '';
    }
}


var get_time = function() {
  $.get('get_time.json', function(res) {
    sync_stuff(res.S1, curstate.S1, '#S1');
    sync_stuff(res.S2, curstate.S2, '#S2');
    sync_stuff(res.S3, curstate.S3, '#S3');
  });
  window.setTimeout(get_time, 600);
}
window.setTimeout(get_time, 600);




function copyToClipboard(element, scr) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
  $("#linkfor").text(scr);
  $("#beendicator").fadeIn();
  window.setTimeout(function() { $("#beendicator").fadeOut(); }, 3000);
}

