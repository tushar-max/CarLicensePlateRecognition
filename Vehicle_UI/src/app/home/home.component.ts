import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APIsService } from '../Service/apis.service';
// import 'jquery';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  public PathUrl = "";
  public loading = false;
  public showForm = false;
  public alertMessage: string = "";
  public messageType: string = "";
  public showPopup: boolean = false;
  public resultValue1: string = 'Result 1';
  public resultValue2: string = 'Result 2';
  public data = [];
  resultData: any = [];
  constructor(private apis: APIsService, private route: Router) { }

  ngOnInit(): void {


  }


  // fetchData() {
  //   this.apis.getResults().subscribe({
  //     next: (response) => {
  //       this.data = response["1"];
  //     },
  //     error(err) {
  //       console.log(err);
  //     },
  //   });
  // }

  validateForm(): boolean {
    if (!this.PathUrl) {
      this.showAlert('Please enter the path of the video.', 'error');
      return false;
    }
    return true;
  }
  showResultValues() {

    this.resultValue1 = 'Updated Result 1';
    this.resultValue2 = 'Updated Result 2';


    this.showPopup = true;
  }

  closePopup() {
    this.showPopup = false;
  }
  getClassForMessageType() {
    return {
      'info': this.messageType === 'info',
      'error': this.messageType === 'error',
      'success': this.messageType === 'success'
    };
  }

  // showAlert(message: string, type: string = 'info') {

  //   }
  // }
  showAlert(message: string, type: string = 'info') {
    this.alertMessage = message;
    this.messageType = type;
    if (type === 'error') {

      // message = `<span style="color: red;">${message}</span>`;
      message = 'Error: ' + message;
    }

    alert(message);
  }
  // handleSubmit(){
  //   this.loading=true;
  //   this.apis.startProcessing(this.PathUrl).subscribe({
  //     next:(response)=>{
  //       console.log(response);
  //       this.loading=false;
  //     },
  //     error(err) {
  //       console.log(err);
  //     }
  //   })
  // }

  openModal() {

    this.resultData = [
      { license_plate_text: 'Plate 1', entryPoint: 'Entry 1' },
      { license_plate_text: 'Plate 2', entryPoint: 'Entry 2' },

    ];
  }
  handleResults() {
    return this.data.length != 0 && !this.loading;
  }
  handleSubmit() {
    if (this.validateForm()) {
      this.loading = true;
      this.apis.startProcessing(this.PathUrl).subscribe({
        next: (response) => {
          console.log(response);  
          this.data = response["1"];
          this.loading = false;
          console.log(this.data);
          this.showAlert('Processing ended successfully', 'success');
        },
        error: (err) => {
          this.loading = false;
          if (err.error && err.error.error) {
            this.showAlert(err.error.error, 'error');
          } else {
            this.showAlert('An error occurred during processing.', 'error');
          }
        }
        });  
     }
  }
}
//   handleSubmit() {
//     if (this.validateForm()) {
//       this.loading = true;
//       this.apis.startProcessing(this.PathUrl).subscribe({
//         next: (response) => {
//           console.log(response);
//           if (response[0] == 'Error') {
//             this.loading = false;
//             this.showAlert('An error occurred during processing.', 'error');
//           }
//           else {
//             this.data = response["1"];
//             this.loading = false;
//             console.log(this.data);
//             this.showAlert('Processing ended successfully', 'success');
//           }
//         },
//         error: (err) => {
//           console.log(err);
//           this.loading = false;
//           this.showAlert('An error occurred during processing.', 'error');
//         }
//       });
//     }
//   }
// }
