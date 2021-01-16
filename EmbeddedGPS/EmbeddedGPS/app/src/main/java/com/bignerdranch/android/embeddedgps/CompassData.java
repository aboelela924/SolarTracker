package com.bignerdranch.android.embeddedgps;

public class CompassData {
    public float compassDeg;
    public long time;

    public CompassData(){

    }

    public CompassData(float compassDeg){
        this.compassDeg = compassDeg;
        time = System.currentTimeMillis();
    }
}
