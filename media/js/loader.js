/**
 * Loader for ajax request.
 */

loader = {
    show: function () {
        if (!loader.panel) {
            loader.panel = $('<div id="loader"></div>');
            $('body').append(loader.panel);
        }
        
        loader.panel.show();
    },
    hide: function () {
        if (loader.panel) {
            loader.panel.stop().fadeOut(100);
        }
    }
};
