package com.fyp.fyp01;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class search_engine extends AppCompatActivity {
    ListView list;
    private DatabaseReference reference;
    ArrayList<Document> documents = new ArrayList<Document>();

    TextView src_para;
    ImageView src_but;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_engine);

        src_para = findViewById(R.id.src_para);
        src_but = findViewById(R.id.src_but);
        getData("");

    }

    private void getData(final String para) {
        reference = FirebaseDatabase.getInstance().getReference()
                .child("Requests").child("Active");
        reference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                int count = 0;
                for(DataSnapshot ds: dataSnapshot.getChildren()){
                    Document req = ds.getValue(Document.class);

                    if(req.getService()==5 && para.isEmpty()) {
                        count += 1;
                        documents.add(req);
                    }
                    else if(req.getService()==5 && src_para(para, req.getKeypharses())){
                        count += 1;
                        documents.add(req);
                    }
                }
                if(count>0){
                    setAdapter();
                }
                Toast.makeText(search_engine.this, "Content is present: " + count, Toast.LENGTH_SHORT).show();
//                    sendNotification();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    private void setAdapter() {
        Log.i("Size: ", "setAdapter: " + documents.size());
        MyListAdapter adapter=new MyListAdapter(this, documents);
        list=(ListView)findViewById(R.id.listView);
        list.setAdapter(adapter);

        list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                // TODO Auto-generated method stub

                Intent i = new Intent(search_engine.this,Final_view.class);
                i.putExtra("sampleObject", documents.get(position));
                Log.i("Intent", "onCreate: " + documents.get(position).getDocument_name());
                startActivity(i);

                if (position == 0) {
                    Toast.makeText(search_engine.this, "Working", Toast.LENGTH_SHORT).show();
                    Log.i("Position: ", "onItemClick: " + documents.get(position).toString());
                }
            }
        });
    }

    public void src_engine(View view) {
        documents.clear();
        MyListAdapter adapter=new MyListAdapter(this, documents);
        list=(ListView)findViewById(R.id.listView);
        list.setAdapter(adapter);
        String src = src_para.getText().toString();
        getData(src);
    }

    private boolean src_para(String para, String keypharses) {
        String temp = keypharses.substring(1, keypharses.length() - 1);
        String[] keywords = temp.split(",");
//        Log.i("Src-me", "src_para: " + para + " " + temp);
        for(int i=0; i<keywords.length; i++){
//            if( i == 0)
//                Log.i("Src", "src_para: " + keywords[i]  + para);
            if(keywords[i].trim().toLowerCase().contains(para.trim().toLowerCase()))
                return true;
        }

        return false;
    }
}
