
var rowNu = 0; //номер ряда отображенного у клиента

function firstRequest(){                                                            //10 last srings of history 4 the first time

	$.getJSON("server/server.py", {"action": "newchat", "row": rowNu}, processmsg); //request
			
		function processmsg(data){											//parse and insert data from server
		
			for (var i=0; i< data.actions.length; i++){
			
				rowNu = +(data.row); 	// position save
			
				var info = data.actions[i].name + ": " + data.actions[i].message; //text output
				$("#chatbox").append(info+"<br>");
				
			}	
			
		};
};

function sendRequest(){		//

	var oldscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //scroll

	$.getJSON("server/server.py", {"action": "sendhis", "row": rowNu}, processmsg); //request
		
		function processmsg(data){											//parse and insert data from server
		
			for (var i=0; i< data.actions.length; i++){
			
				rowNu = +(data.row);                              // row save
				var info = data.actions[i].name + ": " + data.actions[i].message; //text output
				$("#chatbox").append(info+"<br>");
				
				var newscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //Autoscroll to bottom of div
				if(newscrollHeight > oldscrollHeight){
					$("#chatbox").animate({ scrollTop: newscrollHeight }, 'normal'); 
				}

			}	
			
		};
		
	
};

$(document).ready(function(){

	firstRequest(); // запрос на получение 10 последних строк переписки

	var Name = prompt ('What is your name?','Grisha');

	setInterval (sendRequest, 2500);    // опрос сервера
	
		
	$("#exit").click(function(){		
		
	});	
	
	$("#submitmsg").click(function(){		
	
		var msg = $.trim($('#usermsg').val());    // получение сообщения из input
		
		var oldscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //scroll

		$.getJSON("server/server.py", {"action": "sendmsg", "name": Name, "message": msg, "row": rowNu}, processmsg); //request
		
			function processmsg(data) { 											//parse and insert data from server
				
				rowNu = +(data.row); //сохранение ряда
				
				var info = data.actions.name + ": " + data.actions.message; //вывод сообщения
				$("#chatbox").append(info+"<br>");
				
				var newscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //Autoscroll to bottom of div
				if(newscrollHeight > oldscrollHeight){
					$("#chatbox").animate({ scrollTop: newscrollHeight }, 'normal'); 
				}
			};
		
					
	});
	
});