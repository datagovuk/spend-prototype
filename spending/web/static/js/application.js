/* global $ */
/* global GOVUK */

// Warn about using the kit in production
if (
  window.sessionStorage && window.sessionStorage.getItem('prototypeWarning') !== 'false' &&
  window.console && window.console.info
) {
  window.console.info('GOV.UK Prototype Kit - do not use for production')
  window.sessionStorage.setItem('prototypeWarning', true)
}

$(document).ready(function () {
  // Use GOV.UK shim-links-with-button-role.js to trigger a link styled to look like a button,
  // with role="button" when the space key is pressed.
  GOVUK.shimLinksWithButtonRole.init()

  // Show and hide toggled content
  // Where .multiple-choice uses the data-target attribute
  // to toggle hidden content
  var showHideContent = new GOVUK.ShowHideContent()
  showHideContent.init()

  var showHide = new ShowHide()
  showHide.init()
})

var ShowHide = function() {
  this.selector = '.showHide'
  this.controlSelector = '.showHide-control'
  this.contentSelector = '.showHide-content'
  this.openSelector = '.showHide-open-all'
  this.allOpen = false;
}

ShowHide.prototype = {
  toggle : function(event) {
    var parentShowHide = $(event.target).parents(this.selector)
    var isOpen = parentShowHide.data("isOpen")
    parentShowHide.data("isOpen", !isOpen)
    parentShowHide.find(this.contentSelector).toggle()
    parentShowHide.find(this.controlSelector).html(isOpen? '+' : '-');
  },
  toggleAll : function(event) {
    var showHideDataLinks = $(event.target).parents('.data-links')
    event.preventDefault()
    var allOpen = $(event.target).data("allOpen")
    console.log(allOpen)
    if (allOpen) {
      showHideDataLinks.find(this.selector).data('isOpen', false)
      showHideDataLinks.find(this.contentSelector).hide()
      showHideDataLinks.find(this.controlSelector).html('+')
      $(event.target).data("allOpen", false)
      $(event.target).text('Open all')

    } else {
      showHideDataLinks.find(this.selector).data('isOpen', true)
      showHideDataLinks.find(this.contentSelector).show()
      showHideDataLinks.find(this.controlSelector).html('-')
      $(event.target).data("allOpen", true)
      $(event.target).text('Close all')
    }

  },

  init : function() {
    $(this.controlSelector).on('click', this.toggle.bind(this))
    $(this.openSelector).on('click', this.toggleAll.bind(this))
    $(this.selector).data("isOpen", false)
    $(this.openSelector).data("allOpen", false)
  }
}

function do_switch(previewer, appender, tab){
  $(previewer).empty().append($(appender).html());
  $('.tab').each(function(i, elem){
    $(elem).addClass('inactive');
    $(elem).removeClass('active');
  });
  $(tab).parent().removeClass('inactive');
  $(tab).parent().addClass('active');
  $(document).click();
  return false;
}
