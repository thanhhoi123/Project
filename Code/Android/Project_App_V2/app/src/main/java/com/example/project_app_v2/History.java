package com.example.project_app_v2;

import java.util.ArrayList;

public class History {
    public int id;
    public String date;
    public String time;
    public String ratelogo1;
    public String ratelogo2;

    public History(){}
    public History(int id, String date, String time, String ratelogo1, String ratelogo2) {
        this.id = id;
        this.date = date;
        this.time = time;
        this.ratelogo1 = ratelogo1;
        this.ratelogo2 = ratelogo2;
    }

    public String getRatelogo1() {
        return ratelogo1;
    }

    public void setRatelogo1(String ratelogo1) {
        this.ratelogo1 = ratelogo1;
    }

    public String getRatelogo2() {
        return ratelogo2;
    }

    public void setRatelogo2(String ratelogo2) {
        this.ratelogo2 = ratelogo2;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }
}
