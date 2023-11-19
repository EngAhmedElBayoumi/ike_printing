function addMatrial() {
  var tableBody = document.getElementById("tableBodyMatrial");
  var newRow = document.createElement("tr");
    var matrial = document.getElementById("MatrialSelect").value;
    var percent = document.getElementById("PercentSelect").value;
  var rowContent = `
    <td><p>${matrial}</p></td>
      <td><p>${percent}</p></td>
    <td>
      <button onclick="removeRowmatrial(this)" class="btn btn-danger" style="color: #fff">Remove</button>
    </td>
  `;
  newRow.innerHTML = rowContent;
  tableBody.appendChild(newRow);
}
        
        function removeRowmatrial(button) {
  var row = button.closest("tr");
  row.remove();
}
   
        
        
        
