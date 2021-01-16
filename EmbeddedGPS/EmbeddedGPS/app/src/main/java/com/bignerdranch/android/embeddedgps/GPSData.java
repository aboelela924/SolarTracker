package com.bignerdranch.android.embeddedgps;

public class GPSData {

    public double latitude;
    public double longitude;
    public double altitude;

    public GPSData(){

    }

    public GPSData(double latitude, double longitude, double altitude) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.altitude = altitude;
    }
}
