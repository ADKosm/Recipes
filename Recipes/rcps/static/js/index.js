$( document ).ready(function() {
    var ingId = 1;
    var eqId = 1;
    var getId = function(str){
        var idReg = /\w+-\w+-(\d+)/;
        return parseInt(str.replace(idReg, "$1"), 10);
    };

    var setLiveQueryIng = function(id) {
         $("#ing"+id).find("input").keypress(function(e) {
             if (e.which == 13) {
                $("#live-query-ing").html("");
                return false;    //<---- Add this line
             }
         });
         $("#ing"+id).find("input").on("input", function(){
            var pref = $(this).val();
            $.ajax({
                url: "live_query_ing",
                data: { prefix: pref},
                dataType: "json"
            }).done(function(msg){
                $("#live-query-ing").html("");
                $.each(msg.vars, function(index, value){
                    $("#live-query-ing").append("<option>"+value+"</option>");
                });
            });
        });
    }

    var setLiveQueryEq = function(id) {
         $("#eq"+id).find("input").keypress(function(e) {
             if (e.which == 13) {
                $("#live-query-eq").html("");
                return false;    //<---- Add this line
             }
         });
        $("#eq"+id).find("input").on("input", function(){
            var pref = $(this).val();
            $.ajax({
                url: "live_query_eq",
                data: { prefix: pref},
                dataType: "json"
            }).done(function(msg){
                $("#live-query-eq").html("");
                $.each(msg.vars, function(index, value){
                    $("#live-query-eq").append("<option>"+value+"</option>");
                });
            });
        });
    }

    setLiveQueryIng(ingId);
    setLiveQueryEq(eqId);

    $("#add-ing-button").click(function(){
        ingId++;
        $("#ing-list").append("<div class='input-group ing-element' id='ing"+ingId+"'></div>");
        $("#ing"+ingId).loadTemplate($("#ing-list-element"), {butid: "ing-but-"+ingId});
        $("#ing-but-"+ingId).click(function(){
            var myId = getId($(this).attr('id'));
            $("#ing"+myId).remove();
        });
        setLiveQueryIng(ingId);
    });

    $("#add-eq-button").click(function(){
        eqId++;
        $("#eq-list").append("<div class='input-group eq-element' id='eq"+eqId+"'></div>");
        $("#eq"+eqId).loadTemplate($("#eq-list-element"), {butid: "eq-but-"+eqId});
        $("#eq-but-"+eqId).click(function(){
            var myId = getId($(this).attr('id'));
            $("#eq"+myId).remove();
        });
        setLiveQueryEq(eqId);
    });

    $("#send-but").click(function(){
        var ingredientCSV = "";
        var equipmentCSV = "";
        var presenceCSV = $("#presence").val() == "в наличии" ? 1 : 0;

        $("#ing-list").find("input").each(function(){
            ingredientCSV+= $(this).val()+",";
        });
        $("#eq-list").find("input").each(function(){
            equipmentCSV+= $(this).val()+",";
        });

        var requestStr = "search?ings="+ingredientCSV+"&equips="+equipmentCSV+"&pres="+presenceCSV;

        window.location = location.href+requestStr
    });

});