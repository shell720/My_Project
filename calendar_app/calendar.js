const button = document.getElementById("make");

button.addEventListener( "click", func =() =>{
  var year  = document.getElementById("year").value;
  var month = document.getElementById("month").value-1; //どうやら一つずれている
  var day   = document.getElementById("day").value;

  var output = document.getElementById("calendar")

  date = new Date(year, month, day);
  FirstDay = new Date(year, month, 1);
  FirstSpace = FirstDay.getDay();
  FinalDay   = new Date(year, month+1, 0);
  endSpace = 7-(FirstSpace+FinalDay.getDate())%7
  //endDay = FinalDay.getDate()
  shuturyoku = "<table id=\"calendar\"> <tr> <th id=Sun>日</th>  <th>月</th> <th>火</th> <th>水</th> <th>木</th>";
  shuturyoku += "<th>金</th> <th id=Sat>土</th> </tr></table>";
  
  shuturyoku += "<tr>"
  for (let i =0; i<FirstSpace; i++){
    shuturyoku += " <td> </td>";
  }
  for (let i =1; i<=FinalDay.getDate(); i++){
    if (i == day){
      shuturyoku += "<td id=today>"+i+"</td>";
    } else {
      shuturyoku += "<td>"+i+"</td>";
    }
    if ((i+FirstSpace)%7==0){
      shuturyoku += "</tr><tr>"
    }
    
  }
  for (let i =0; i<endSpace; i++){
    shuturyoku += " <td> </td>";
  }
  shuturyoku += "</tr>"
  output.innerHTML = shuturyoku;
}
);