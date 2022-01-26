package com.example.project_app_v2;


import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.FirebaseApp;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HomeActivity extends AppCompatActivity {
    private LoadingDialog loadingDialog;
    private String user;
    private DatabaseReference mDatabase;
    private TextView dateNow;
    private RecyclerView rcvPost;
    private HistoryAdapter postAdapter;
    private List<History> postList;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        this.setTitle("History");

        loadingDialog = new LoadingDialog(HomeActivity.this);
        rcvPost = findViewById(R.id.RcvHistory);
        rcvPost.setLayoutManager(new LinearLayoutManager(this));
        postList = new ArrayList<History>();
        postAdapter = new HistoryAdapter(postList, this);
        rcvPost.setAdapter(postAdapter);

        dateNow = findViewById(R.id.textView2);
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy", Locale.getDefault());
        dateNow.setText(sdf.format(new Date()));
        FirebaseApp.initializeApp(this);

        showPost();
    }
    public void showPost(){
        loadingDialog.startLoadingDialog();
        getAllPostMessage();
    }
    public void getAllPostMessage(){
        mDatabase = FirebaseDatabase.getInstance().getReference("");
        mDatabase.orderByChild("date").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                postList.clear();
                for(DataSnapshot item:snapshot.getChildren()){
                    History data = item.getValue(History.class);
                    postList.add(new History(data.getId(),data.getDate(),data.getTime(),data.getRatelogo1(),data.getRatelogo2()));
                }
                loadingDialog.dismissDialog();
                postAdapter.notifyDataSetChanged();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                loadingDialog.dismissDialog();
                Toast.makeText(HomeActivity.this,"Dữ liệu trống",Toast.LENGTH_SHORT).show();
            }
        });
    }
    protected void closeApp(){
        AlertDialog alertDialog = new AlertDialog.Builder(this)
                .setMessage("Đăng xuất khỏi tài khoản ?")
                .setPositiveButton("YES", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        Toast.makeText(HomeActivity.this,"Bạn đã đăng xuất !",Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(HomeActivity.this,MainActivity.class);
                        startActivity(intent);
                    }
                })
                .setNegativeButton("CANCEL", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {

                    }
                }).show();
    }
    @Override
    public void onBackPressed() {
        closeApp();
    }
}