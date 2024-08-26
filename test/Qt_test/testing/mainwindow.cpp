#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <stdio.h>

int currPos = 1;
char item_name[100];

/*

Plan:
1) Prob just have 9 buttons for now, worry about "adding" later
2) Before "adding" at least have loadable preset to test out other features

GUI Changes from proposal
- Add item will always be visible button


*/


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    ui->gridLayout->addWidget(new QPushButton("Add Item"), currPos/3, currPos%3);
    currPos++;
}

void MainWindow::on_pushButton_2_clicked()
{
    sprintf(item_name, "Item %i", currPos);
    ui->gridLayout->addWidget(new QPushButton(item_name), currPos/3, currPos%3);
    currPos++;
}

// USE A STACK AS FSM OR WHATEVER

/*
#include "mainwindow.h"
#include <iostream>

#include <QWidget>
#include <QDebug>
#include <QVBoxLayout>
#include <QPushButton>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
    , row(0)
    , column(0)
{
    btnLayout = new QGridLayout();
    for(int i = 0; i < 9; i++) {
        QPushButton *b = new QPushButton();
        b->setText(QString::number(i));
        b->setFixedSize(20, 20);
        btns.push_back(b);
        btnLayout->addWidget(b,row, i);
    }
    copyButton = new QPushButton();
    copyButton->setText("Copy!");
    btnsWidget = new QWidget();
    btnsWidget->setLayout(btnLayout);
    connect(copyButton, &QPushButton::clicked, this, &MainWindow::copyButtonClicked);
    mainLayout = new QVBoxLayout();
    mainLayout->addWidget(copyButton);
    mainLayout->addWidget(btnsWidget);
    setLayout(mainLayout);
    qDebug()<< btns.size();
    row++;
}

MainWindow::~MainWindow()
{
}

void MainWindow::copyButtonClicked(){
    int length = (int)btns.size();
    for(int i = 0; i < length; i++) {
        QPushButton *newButton = new QPushButton();
        newButton->setFixedSize(20, 20);
        newButton->setText(btns[i]->text());
        btns.push_back(newButton);
        btnLayout->addWidget(newButton, row, column++);
        if(column % 9 == 0){
            row++;
            column = 0;
        }
    }
}

 */
