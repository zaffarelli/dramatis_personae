"use strict";

function dice_initialize(container, size = 400) {

  let canvas = $t.id('canvas');
  canvas.style.width = size + 'px';
  canvas.style.height = size + 'px';
  let label = $t.id('label');
  let set = $t.id('set');
  let explode = false;
  let stack = []
  on_set_change();
  $t.dice.use_true_random = false;

  function on_set_change(ev) {
    //set.style.width = set.value.length + 3 + 'ex';
  }
  // $('#set').off('keyup').on('keyup', on_set_change);
  // $('#set').off('mousedown').on('mousedown', function(ev) {
  //   ev.stopPropagation();
  // });
  // $t.bind(set, 'mouseup', function(ev) {
  //   ev.stopPropagation();
  // });
  // $t.bind(set, 'focus', function(ev) {
  //   $t.set(container, {
  //     class: ''
  //   });
  // });
  // $t.bind(set, 'blur', function(ev) {
  //   $t.set(container, {
  //     class: 'noselect'
  //   });
  // });
  // $t.bind($t.id('clear'), ['mouseup', 'touchend'], function(ev) {
  //   ev.stopPropagation();
  //   set.value = '0';
  //   on_set_change();
  // });
  let params = $t.get_url_params();
  let box = new $t.dice.dice_box(canvas, {
    w: size,
    h: size
  });

  $t.bind(window, 'resize', function() {
    canvas.style.width = size + 'px';
    canvas.style.height = size + 'px';
    box.reinit(canvas, {
      w: size,
      h: size
    });
  });


  function before_roll(vectors, notation, callback) {
    callback();
  }

  function notation_getter() {
    return $t.dice.parse_notation(set.value);
  }

  function after_roll(notation, result) {
    if (params.chromakey || params.noresult) {
      return;
    }
    console.log('notation:');
    console.log(notation);
    console.log('result:');
    console.log(result);

    if (notation.set.length == 1 && notation.set[0] == 'd12') {
      if (result.length == 1) {
        if (result[0] == 12) {
          explode = true;
          console.log("Explode!")
          stack[stack.length] = result[0];
          $t.raise_event($t.id('throw'), 'mouseup');
        } else {
          let res = result.join(' ');
          if (notation.constant) {
            if (notation.constant > 0) {
              res += ' +' + notation.constant;
            } else {
              res += ' -' + Math.abs(notation.constant);
            }
          }
          if (result.length >= 1) res += ' = ' +
            (result.reduce(function(s, a) {
              return s + a;
            }) + notation.constant);
          label.innerHTML = res;
        }

      }
    }

  }

  //box.bind_mouse(container, notation_getter, before_roll, after_roll);
  box.bind_throw($t.id('throw'), notation_getter, before_roll, after_roll);

  // if (params.notation) {
  //   console.log("params notation");
  //   set.value = params.notation;
  // }
  // if (params.roll) {
  //   console.log("roll");
  //   $t.raise_event($t.id('throw'), 'mouseup');
  // }
}
