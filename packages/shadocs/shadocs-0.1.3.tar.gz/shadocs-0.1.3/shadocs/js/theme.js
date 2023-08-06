$( document ).ready(function() {
    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='wy-nav-top']", function() {
      $("[data-toggle='wy-nav-shift']").toggleClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });

    // Close menu when you click a link.
    $(document).on('click', ".wy-menu-vertical .current ul li a", function() {
      $("[data-toggle='wy-nav-shift']").removeClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });

    // Keyboard navigation
    document.addEventListener("keydown", function(e) {
      var key = e.which || e.keyCode || window.event && window.event.keyCode;
      var page;
      switch (key) {
          case 78:  // n
              page = $('[role="navigation"] a:contains(Next):first').prop('href');
              break;
          case 80:  // p
              page = $('[role="navigation"] a:contains(Previous):first').prop('href');
              break;
          case 13:  // enter
              if (e.target === document.getElementById('mkdocs-search-query')) {
                e.preventDefault();
              }
              break;
          default: break;
      }
      if ($(e.target).is(':input')) {
        return true;
      } else if (page) {
        window.location.href = page;
      }
    });

    $(document).on('click', "[data-toggle='rst-current-version']", function() {
      $("[data-toggle='rst-versions']").toggleClass("shift-up");
    });

    // Make tables responsive
    $("table.docutils:not(.field-list)").wrap("<div class='wy-table-responsive'></div>");

    $('table').addClass('docutils');

    /*
     * Custom rtd-dropdown
     */
    toggleCurrent = function (elem) {
        var parent_li = elem.closest('li');
        var menu_li = parent_li.next();
        var menu_ul = menu_li.children('ul');
        parent_li.siblings('li').not(menu_li).removeClass('current').removeClass('with-children');
        parent_li.siblings().find('> ul').not(menu_ul).removeClass('current').addClass('toc-hidden');
        parent_li.toggleClass('current').toggleClass('with-children');
        menu_li.toggleClass('current');
        menu_ul.toggleClass('current').toggleClass('toc-hidden');
    }

    // https://github.com/rtfd/sphinx_rtd_theme/blob/master/js/theme.js
    $('.tocbase').find('.toctree-expand').each(function () {
        var link = $(this).parent();
        $(this).on('click', function (ev) {
            console.log('click expand');
            toggleCurrent(link);
            ev.stopPropagation();
            return false;
        });
        link.on('click', function (ev) {
            console.log('click link');
            toggleCurrent(link);
        });
    });
});

window.SphinxRtdTheme = (function (jquery) {
    var stickyNav = (function () {
        var navBar,
            win,
            stickyNavCssClass = 'stickynav',
            applyStickNav = function () {
                if (navBar.height() <= win.height()) {
                    navBar.addClass(stickyNavCssClass);
                } else {
                    navBar.removeClass(stickyNavCssClass);
                }
            },
            enable = function () {
                applyStickNav();
                win.on('resize', applyStickNav);
            },
            init = function () {
                navBar = jquery('nav.wy-nav-side:first');
                win    = jquery(window);
            };
        jquery(init);
        return {
            enable : enable
        };
    }());
    return {
        StickyNav : stickyNav
    };
}($));

// The code below is a copy of @seanmadsen code posted Jan 10, 2017 on issue 803.
// https://github.com/mkdocs/mkdocs/issues/803
// This just incorporates the auto scroll into the theme itself without
// the need for additional custom.js file.
//
$(function() {
  $.fn.isFullyWithinViewport = function(){
      var viewport = {};
      viewport.top = $(window).scrollTop();
      viewport.bottom = viewport.top + $(window).height();
      var bounds = {};
      bounds.top = this.offset().top;
      bounds.bottom = bounds.top + this.outerHeight();
      return ( ! (
        (bounds.top <= viewport.top) ||
        (bounds.bottom >= viewport.bottom)
      ) );
  };
  if( $('li.toctree-l1.current').length && !$('li.toctree-l1.current').isFullyWithinViewport() ) {
    $('.wy-nav-side')
      .scrollTop(
        $('li.toctree-l1.current').offset().top -
        $('.wy-nav-side').offset().top -
        60
      );
  }
});

$(function() {
 $(".sidebar-scroll").slimScroll({
  width: 'auto', //可滚动区域宽度
  height: '100%', //可滚动区域高度
  size: '10px', //组件宽度
  color: '#000', //滚动条颜色
  position: 'right', //组件位置：left/right
  distance: '0px', //组件与侧边之间的距离
  start: 'top', //默认滚动位置：top/bottom
  opacity: .4, //滚动条透明度
  alwaysVisible: true, //是否 始终显示组件
  disableFadeOut: false, //是否 鼠标经过可滚动区域时显示组件，离开时隐藏组件
  railVisible: true, //是否 显示轨道
  railColor: '#333', //轨道颜色
  railOpacity: .2, //轨道透明度
  railDraggable: true, //是否 滚动条可拖动
  railClass: 'slimScrollRail', //轨道div类名 
  barClass: 'slimScrollBar', //滚动条div类名
  wrapperClass: 'slimScrollDiv', //外包div类名
  allowPageScroll: true, //是否 使用滚轮到达顶端/底端时，滚动窗口
  wheelStep: 20, //滚轮滚动量
  touchScrollStep: 200, //滚动量当用户使用手势
  borderRadius: '7px', //滚动条圆角
  railBorderRadius: '7px' //轨道圆角
 });
});
