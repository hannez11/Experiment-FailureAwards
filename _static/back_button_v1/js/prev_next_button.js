// Source: https://www.jqueryscript.net/other/bootstrap-tabs-carousel.html



function bootstrapTabControl(){
    var i, items = $('.topnav'), pane = $('.toppane'); //class selector modified since initialdecision page has two navbars ; class="nav-link topnav" ; class="tab-pane toppane" ; topnav and toppane were added
    // next
    $('.nexttab').on('click', function(){
        for(i = 0; i < items.length; i++){
            if($(items[i]).hasClass('active') == true){
                break;
            }
        }
        if(i < items.length - 1){
            // for tab
            $(items[i]).removeClass('active');
            $(items[i+1]).addClass('active');
            // for pane
            $(pane[i]).removeClass('show active');
            $(pane[i+1]).addClass('show active');
        }
  
    });
    // Prev
    $('.prevtab').on('click', function(){
        for(i = 0; i < items.length; i++){
            if($(items[i]).hasClass('active') == true){
                break;
            }
        }
        if(i != 0){
            // for tab
            $(items[i]).removeClass('active');
            $(items[i-1]).addClass('active');
            // for pane
            $(pane[i]).removeClass('show active');
            $(pane[i-1]).addClass('show active');
        }
    });
  }
  bootstrapTabControl();
  
  
  function topFunction() { //jumps to top of the page when navbar link is clicked
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }