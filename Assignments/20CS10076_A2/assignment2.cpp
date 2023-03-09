#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>
#include <cmath>
#include "rapidxml.hpp"                                                                              // using rapidxml library for xml parsing
#include <map>
#include <queue>
#include <stack>
  
using namespace std;                                                                                
using namespace rapidxml;

xml_document<> doc;                                                                                 // creating xml document element
xml_node<> *root_node=NULL;

double toRadians(double degree)                                                                     // convert latitude and longitude to radians
{
    double pi = 3.14159265359;
    return (degree * (pi / 180));
}

double crowFlyDistance (double lat1, double lon1, double lat2, double lon2) {                      // calculating crow fly distance between two points given coordinates
    double R = 6371; // km
    double dLat = toRadians(lat2-lat1);
    double dLon = toRadians(lon2-lon1);
    double lat1_r = toRadians(lat1);
    double lat2_r = toRadians(lat2);

    double a = sin(dLat/2) * sin(dLat/2) +
            sin(dLon/2) * sin(dLon/2) * cos(lat1_r) * cos(lat2_r);
    double c = 2 * atan2(sqrt(a), sqrt(1-a));
    double d = R * c;
    return d;
}
// creating a vector of distances from given point to all other points and then sorting the distances for k nearest neighbours
void distancesVector(vector<pair<double,string>>& distances, vector<double> latitudes, vector<double> longitudes, vector<string> IDs, int index) {
    for (int i = 0; i < distances.size(); i++) {
        distances[i] = make_pair(crowFlyDistance(latitudes[index], longitudes[index], latitudes[i], longitudes[i]), IDs[i]);
    }
    sort(distances.begin(), distances.end());
}

int main() {

    cout<<"Parsing map..."<<endl;
    ifstream File("map.osm");                                                                  // opening the file
    vector<char> buffer((istreambuf_iterator<char>(File)), istreambuf_iterator<char>( ));      // reading the file into a buffer
    buffer.push_back('\0');                   
    doc.parse<0>(&buffer[0]) ;                                                                 // parsing the file
    root_node = doc.first_node("osm");
    
    int count_node=0;
    int count_way=0;                                                                           // counters for number of ways and nodes
    vector<string> node_id;                                                                    // storing node IDs as string
    vector<double> node_latitude, node_longitude;                                              // storing latitude and longitude of nodes
    map<string,int> getIndex;                                                                  // create a map from node IDs to node index in vector
    vector<pair<string,string>> node_name;                                                     // storing list of node names with IDs
    vector<pair<string,vector<string>>> way_nodes;                                             // creating a 2D vector of ways and and associated list of nodes
    map<string,vector<pair<string,double>>> node_edges;                                        // creating adjacency list for graph of nodes
    
    cout<<"Loading map data..."<<endl;
    for (xml_node<> *node = root_node->first_node(); node; node = node->next_sibling()) {      // looping through all nodes
        if (node->name() == string("node")) {                                                  // finding nodes
            count_node++;
            node_id.push_back(node->first_attribute("id")->value());                           // storing attributes of nodes
            node_latitude.push_back(stod(node->first_attribute("lat")->value()));
            node_longitude.push_back(stod(node->first_attribute("lon")->value()));
            getIndex[node->first_attribute("id")->value()] = count_node-1;
            for (xml_node<> *child = node->first_node(); child; child = child->next_sibling()) { // capturing name of node
                if (child->name() == string("tag")) {
                    if (child->first_attribute("k")->value() == string("name")) {
                        node_name.push_back(make_pair(node->first_attribute("id")->value(), child->first_attribute("v")->value()));
                    }
                }
            }

        }
        if (node->name() == string("way")) {                                                        // finding ways
            way_nodes.push_back(make_pair(node->first_attribute("id")->value(), vector<string>())); // create a vector of nodes for each way
            count_way++;                                                                            // way found
            for (xml_node<> *way = node->first_node(); way; way = way->next_sibling()) {            // looping through all nodes of a way
                if (way->name() == string("nd")) {
                    string node_id_2 = way->first_attribute("ref")->value();
                    way_nodes[way_nodes.size()-1].second.push_back(node_id_2);
                }
                
            }
        }
    } 
    
    cout<<"Setting up connections..."<<endl;
    for (auto it = way_nodes.begin(); it != way_nodes.end(); it++) {                          //  creating adjacency list for nodes by computing distances between nodes on a way
        for (int i = 0; i < it->second.size()-1; i++) {
            
                
            int index1, index2;
            index1=getIndex[it->second[i]];
            index2=getIndex[it->second[i+1]];
            double weight=crowFlyDistance(node_latitude[index1], node_longitude[index1], node_latitude[index2], node_longitude[index2]);
              
            node_edges[it->second[i]].push_back(make_pair(it->second[i+1], weight));
            node_edges[it->second[i+1]].push_back(make_pair(it->second[i], weight));
 
            
        }
        
    }

    int userChoice;                                                                            // storing user choice 
    cout<<"Hello! Welcome to the Kharagpur OSM Map Parser!\n";
    cout<<"If you want to know the total number of nodes and ways, and to search for a particular element, enter 1.\n";
    cout<<"If you want to find a particular number of closest nodes (using crow-fly distance) from a node, enter 2.\n";
    cout<<"If you want to find the closest node from a particular node along recognised way(s), enter 3.\n";
    cout<<"If you want to exit, enter 4.\n";
    cin>>userChoice;
   
    while(userChoice!=4) {                                                                                   // creating the three use cases
        if (userChoice==1) {
            cout << "Total number of nodes: " << count_node << "\n";                                         // output number of nodes and ways
            cout << "Total number of ways: " << count_way << "\n";

            cout<< "Enter name or substring of name of the element you want to search for: ";                // taking input for searching string
            string userInput;
            cin>>userInput;
            int flag=0;
            for (int i = 0; i < node_name.size(); i++) {                                                    // looping through all names of nodes
                if (node_name[i].second.find(userInput) != string::npos) {                    
                    flag=1;                                                                                 // output details for node found and repeated for all matches                                                                                       
                    int index= getIndex[node_name[i].first];
                    cout << "Node found.\n";
                    cout << "Node ID: "<<node_name[i].first<<"\n";
                    cout << "Node name: "<<node_name[i].second<<"\n";
                    cout << "Node latitude and longitude: "<<node_latitude[index]<<" "<<node_longitude[index]<<"\n";
                    
                }
            } 
            if (flag==0) {                                                                                    // report if no node found
                cout << "No node found.\n";
            }           
        }
         
        else if (userChoice==2) {                                                                            // finding k nearest neighbours
            int k;
            int k_min=1;                  
            int k_max=count_node-1;
            cout << "Enter the number of closest nodes you want to find. k ranges from " << k_min << " to " << k_max << ": ";
            cin >> k;
            if (k>k_max || k<k_min) {                                                                       // checking if k is in range
                cout << "Invalid input.\n";
            }
            else {
                cout<<"Enter the node ID: ";
                string nodeFind;
                cin>>nodeFind;
                int index = find(node_id.begin(), node_id.end(), nodeFind) - node_id.begin();            // finding index of node 
                if (index == node_id.size()) {                                                           // checking if valid ID entered
                    cout << "Invalid input.\n";
                }
                else {
                    cout<<"Calculating closest nodes...\n";
                    vector<pair<double,string>> distances(node_id.size());                               // computing distance between node and all other nodes
                    distancesVector(distances, node_latitude, node_longitude, node_id, index);
                    cout<<"The closest "<<k<<" nodes are:\n";
                    for (int i = 1; i <= k; i++) {                                                      // outputing k nearest nodes (excluding self)
                        
                        cout << "Node ID:" <<distances[i].second << ", Node distance: " << distances[i].first <<" km, Node latitude: "<<node_latitude[i]<<", Node longitude: "<<node_longitude[i]<<endl;
                    }
                }
                
            }
        }

        else if (userChoice==3) {                                                                      // shortest paths along ways
            cout << "Enter the ID of the source node: ";                                               // capturing source and destination nodes
            string source;
            cin>>source;
            cout << "Enter the ID of the destination node: ";
            string destination;
            cin>>destination;
            if (find(node_id.begin(), node_id.end(), source) == node_id.end() || find(node_id.begin(), node_id.end(), destination) == node_id.end()) {
                cout << "Invalid source (or) destination.\n";
            }
            
            else {
                cout<<"Calculating shortest path...\n";
                map<string,bool> visited;                                                                  // Apply Dijkstra's algorithm to find shortest path between source and destination
                map<string,double> distance;
                map<string,string> parent;
                for (auto id:node_id) {
                    visited[id]=false;
                    distance[id]=1e9;
                    parent[id]="";
                }
                distance[source]=0;
                priority_queue<pair<double,string>, vector<pair<double,string>>, greater<pair<double,string>>> pq;
                pq.push(make_pair(0,source));
                while(!pq.empty()) {
                    string u=pq.top().second;
                    pq.pop();
                    if (visited[u]) {
                        continue;
                    }
                    visited[u]=true;
                    for (int i = 0; i < node_edges[u].size(); i++) {
                        string v=node_edges[u][i].first;
                        double w=node_edges[u][i].second;
                        if (distance[u]+w<distance[v]) {
                            distance[v]=distance[u]+w;
                            parent[v]=u;
                            pq.push(make_pair(distance[v],v));
                        }
                    }
                }
                if (distance[destination]==1e9) {
                    cout << "No path found.\n";
                }
                else {
                    cout << "The shortest path from " << source << " to " << destination << " is: " << endl;
                    string u=destination;
                    stack<string> path;
                    while(u!=source) {
                        path.push(u);
                        u=parent[u];
                    }
                    path.push(source);
                    while(!path.empty()) {
                        int index= getIndex[path.top()];
                        cout<<"Node ID: "<<path.top()<<", Node latitude: "<<node_latitude[index]<<", Node longitude: "<<node_longitude[index]<<endl;
                        //cout << path.top() << " ";
                        path.pop();
                    }
                    cout << "\nThe distance is: " << distance[destination] <<" km\n";
                }
            }
        }

        else {
            cout << "Invalid input.\n";
            
        }
        cout<<"If you want to know the total number of nodes and ways, and to search for a particular element, enter 1.\n";
        cout<<"If you want to find a particular number of closest nodes (using crow-fly distance) from a node, enter 2.\n";
        cout<<"If you want to find the closest node from a particular node along recognised way(s), enter 3.\n";
        cout<<"If you want to exit, enter 4.\n";
        cin>>userChoice;
    }

    cout<<"Thank you for using this platform. Have a nice day!\n";
    
}
