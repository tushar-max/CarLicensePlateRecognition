import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class APIsService {

  public resultData = [];
  baseApiUrl:string='http://127.0.0.1:5000'
  constructor(private http:HttpClient) { }
  
  startProcessing(path:any):Observable<any>{
    return this.http.post<any>(this.baseApiUrl+'/getPath',JSON.stringify(path));
  }

  getResults():Observable<any>{
    return this.http.get<any>(this.baseApiUrl+'/getData');
  }

  setResultData(data:[]){
    this.resultData=data;
  }
  getResultData(){
    return this.resultData;
  }
}
