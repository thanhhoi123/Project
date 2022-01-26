package com.example.project_app_v2;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class ImageStorage extends AppCompatActivity {
    private LoadingDialog loadingDialog;
    private static String position;
    private RecyclerView recyclerView1;
    private RecyclerView recyclerView2;
    private ArrayList<Image> list1;
    private ArrayList<Image> list2;
    private ImageAdapter adapter1;
    private ImageAdapter adapter2;
    private TextView textlogo1;
    private TextView textlogo2;

    private DatabaseReference root1;
    private DatabaseReference root2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_storage);
        getSupportActionBar().hide();

        Intent receive = getIntent();
        if(receive != null){
            position = receive.getStringExtra("position");
        }
        loadingDialog = new LoadingDialog(ImageStorage.this);
        root1 = FirebaseDatabase.getInstance().getReference(position+"/logo1");
        root2 = FirebaseDatabase.getInstance().getReference(position+"/logo2");
        loadingDialog.startLoadingDialog();
        recyclerView1 = findViewById(R.id.RcvLogo1);
        recyclerView2 = findViewById(R.id.RcvLogo2);
        textlogo1 = findViewById(R.id.logo1);
        textlogo2 = findViewById(R.id.logo2);
        recyclerView1.setHasFixedSize(true);
        recyclerView2.setHasFixedSize(true);
        recyclerView1.setLayoutManager(new GridLayoutManager(this,2));
        recyclerView2.setLayoutManager(new GridLayoutManager(this,2));
        list1 = new ArrayList<>();
        list2 = new ArrayList<>();
        adapter1 = new ImageAdapter(this, list1);
        adapter2 = new ImageAdapter(this, list2);
        recyclerView1.setAdapter(adapter1);
        recyclerView2.setAdapter(adapter2);

        root1.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for (DataSnapshot dataSnapshot : snapshot.getChildren()){
                    Image model = dataSnapshot.getValue(Image.class);
                    list1.add(model);
                }
                adapter1.notifyDataSetChanged();
            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {
            }
        });
        root2.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for (DataSnapshot dataSnapshot : snapshot.getChildren()){
                    Image model = dataSnapshot.getValue(Image.class);
                    list2.add(model);
                }
                adapter2.notifyDataSetChanged();
            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {
            }
        });
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                textlogo1.setText("Logo 1 ("+list1.size()+")");
                textlogo2.setText("Logo 2 ("+list2.size()+")");
                loadingDialog.dismissDialog();
            }
        },2000);
    }
}