package com.fyp.fyp01;

import java.io.Serializable;

public class Document implements Serializable {
    public String document_name;
    public String document_path;
    public String author;
    public String year;
    public int service = 1;
    public String document_json="";
    public String keypharses="";

    public String getDocument_name() {
        return document_name;
    }

    public void setDocument_name(String document_name) {
        this.document_name = document_name;
    }

    public String getDocument_path() {
        return document_path;
    }

    public void setDocument_path(String document_path) {
        this.document_path = document_path;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getYear() {
        return year;
    }

    public void setYear(String year) {
        this.year = year;
    }

    public void setService(int service) {
        this.service = service;
    }

    public void setDocument_json(String document_json) {
        this.document_json = document_json;
    }

    public void setKeypharses(String keypharses) {
        this.keypharses = keypharses;
    }

    public Document(){

    }

    public Document(String document_name, String document_path, String author, String year){
        this.document_name = document_name;
        this.document_path = document_path;
        this.author = author;
        this.year = year;
    }

    public int getService() {
        return service;
    }

    public String getDocument_json() {
        return document_json;
    }

    public String getKeypharses() {
        return keypharses;
    }
}
