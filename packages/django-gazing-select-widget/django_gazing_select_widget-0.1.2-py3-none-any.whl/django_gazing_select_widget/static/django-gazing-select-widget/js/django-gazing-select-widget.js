(function($){
    $.fn.gazing_select = function(){
        return $(this).each(function(){
            var selector = $(this);
            var this_field_name = selector.attr("data-this-field-name");
            var gazing_field_name = selector.attr("data-gazing-field-name");
            var gazing_related = selector.attr("data-gazing-related") == "true";
            var hide_all_if_empty = selector.attr("data-hide-all-if-empty") == "true";
            var this_id = selector.attr("id");
            var prefix = this_id.substring(0, this_id.length - this_field_name.length);
            var gazing_field = $("#id_" + gazing_field_name);
            if(gazing_related){
                gazing_field = $("#" + prefix + gazing_field_name);
            }
            var hide_all_options = function(){
                selector.find("> option, > optgroup > option").each(function(index, option){
                    if($(option).attr("value")){
                        $(option).wrap("<span />");
                    }
                });
            };
            var show_all_options = function(){
                selector.find("span > option").unwrap();
            }
            var fix_optgroup = function(){
                selector.find("> optgroup").each(function(){
                    if($(this).children("option").length < 1){
                        $(this).wrap("<span />");
                    }
                });
                selector.find("span > optgroup").each(function(){
                    if($(this).children("option").length > 0){
                        $(this).unwrap();
                    }
                });
            };
            var do_change = function(){
                var value = gazing_field.val();
                if(value){
                    selector.find("option").each(function(index, option){
                        try{
                            data_for = JSON.parse($(option).attr("data-for"));
                        }catch(e){
                            data_for = [];
                        }
                        if(!data_for){
                            data_for =[];
                        }
                        if(data_for.includes(value)){
                            $(option).unwrap("span");
                        }else{
                            if($(option).parent().prop("tagName") != "SPAN" && $(option).attr("value") != ""){
                                $(option).wrap("<span />");
                            }
                        }
                    });
                }else{
                    if(hide_all_if_empty){
                        hide_all_options();
                    }else{
                        show_all_options();
                    }
                }
                fix_optgroup();
            };
            $(gazing_field).change(function(){
                do_change();
            });
            do_change();
        });
    };

    $(document).ready(function(){
        $(".django-gazing-select-widget").gazing_select();
        $(document).bind("DOMNodeInserted", function(e){
            if($(e.target).is(".django-gazing-select-widget")){
                $(e.target).gazing_select();
            }else{
                $(e.target).find(".django-gazing-select-widget").gazing_select();
            }
        });
    });
})(jQuery);