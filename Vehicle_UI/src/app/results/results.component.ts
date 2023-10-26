// import { Component } from '@angular/core';
// import { APIsService } from '../Service/apis.service';

// @Component({
//   selector: 'app-results',
//   templateUrl: './results.component.html',
//   styleUrls: ['./results.component.css']
// })
// export class ResultsComponent {
//   public data = [];
//   constructor(private apis:APIsService){}
//   ngOnInit():void{
//     this.apis.getResults().subscribe({
//       next:(response)=>{
//         console.log(response);
//         this.data=response;
//       },
//       error(err) {
//         console.log(err);
//       },
//     })
//     this.data = this.apis.getResultData();
//     console.log(this.data);
    
//   }
// }
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIsService } from '../Service/apis.service';

@Component({
    selector: 'app-results',
    templateUrl: './results.component.html',
    styleUrls: ['./results.component.css']
  })


  export class ResultsComponent {
  
    public data = [];
  
    constructor(private apis:APIsService){}
  
    ngOnInit():void{
  
      this.apis.getResults().subscribe({
  
        next:(response)=>{
  
          console.log(response["1"]);
  
          this.data=response["1"];

          this.data.reverse();
  
          // for (let index = 0; index < this.data.length; index++) {
  
          //   // this.data[index]['entryPoint']['$date'] = this.getDate(this.data[index]['entryPoint']['$date'])
  
           
  
          // }
  
         
  
        },
  
        error(err) {
  
          console.log(err);
  
        },
  
      })    
  
    }
  
    getDate(date:any){
  
      return new Date(date.toLocaleDateString());
  
    }
  
  }


