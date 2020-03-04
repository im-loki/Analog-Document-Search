package com.fyp.fyp01;

import android.app.Activity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.sql.Array;
import java.util.ArrayList;

public class MyListAdapter extends ArrayAdapter<Document> {

    private final Activity context;
    ArrayList<Document> documents;

    public MyListAdapter(Activity context, ArrayList<Document> documents) {
        super(context, R.layout.mylist, documents);
        this.context=context;
        this.documents = documents;
        if(documents != null)
            Log.i("Size: ", "MyListAdapter: " + this.documents.size());
    }

    public View getView(int position, View view, ViewGroup parent) {
        LayoutInflater inflater=context.getLayoutInflater();
        View rowView=inflater.inflate(R.layout.mylist, null,true);

        TextView titleText = (TextView) rowView.findViewById(R.id.name);
        TextView subtitleText = (TextView) rowView.findViewById(R.id.author);
        TextView keyText = rowView.findViewById(R.id.keywords);
        ImageView image = rowView.findViewById(R.id.icon);

        titleText.setText(documents.get(position).getDocument_name());
        subtitleText.setText(documents.get(position).getAuthor());
        keyText.setText(documents.get(position).getKeypharses());
        Picasso.get().load(documents.get(position).getDocument_path()).into(image);
        return rowView;
    }
}
