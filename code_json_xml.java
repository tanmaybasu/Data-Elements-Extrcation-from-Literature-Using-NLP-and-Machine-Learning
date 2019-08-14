/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jsonparser;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author aka324
 */
public class printInclExcl {
    
    public static void main(String argsv[]) throws FileNotFoundException, IOException, ParseException{
        //results_cochrane_HF.json
        System.out.println("reading");
        String fileName = "CDSR.json";
        FileReader fileReader = new FileReader(fileName);
        List<String> orderL = new ArrayList<String>();
        // Always wrap FileReader in BufferedReader.
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        String line = "";
        
        StringBuilder str = new StringBuilder();
        while ((line = bufferedReader.readLine()) != null) {
            str = str.append(line + " ");
            if(line.contains("\"Methods\":"))
                orderL.add("Methods");
            else if(line.contains("\"Interventions\":"))
                orderL.add("Interventions");
            else if(line.contains("\"Notes\":"))
                orderL.add("Notes");
            else if(line.contains("\"Outcomes\":"))
                orderL.add("Outcomes");
            else if(line.contains("\"Participants\":"))
                orderL.add("Participants");
            else if(line.contains("\"Label\":"))
                orderL.add("Label");
            else if(line.contains("\"Filename\":"))
                orderL.add("Filename");
            
        }
        String jsonText = str.toString();
        System.out.println("Done");
        
        
        JSONParser parser = new JSONParser();
        KeyFinder finder = new KeyFinder();
        
        //List<String> getValues(String lookFor,String jsonText)
        
        List<String> MethodsL = getValues("Methods",jsonText);
        List<String> InterventionsL = getValues("Interventions",jsonText);
        List<String> NotesL = getValues("Notes",jsonText);
        List<String> OutcomesL = getValues("Outcomes",jsonText);
        List<String> ParticipantsL = getValues("Participants",jsonText);
        List<String> LabelL = getValues("Label",jsonText);
        List<String> FilenameL = getValues("Filename",jsonText);
        
        
        
        
        List<fName> fnL = new ArrayList<fName>();
        List<studies> stuL = new ArrayList<studies>();
        studies currSt = new studies();
        fName currFN = new fName();
        for(String ptr : orderL){
            if(ptr.equalsIgnoreCase("Methods")){
                currSt.method = MethodsL.get(0);
                MethodsL.remove(0);
            }
            else if (ptr.equalsIgnoreCase("Interventions")) {
                currSt.interventions = InterventionsL.get(0);
                InterventionsL.remove(0);
            }
            else if (ptr.equalsIgnoreCase("Notes")) {
                currSt.notes = NotesL.get(0);
                NotesL.remove(0);
            }
            else if (ptr.equalsIgnoreCase("Outcomes")) {
                currSt.outcomes = OutcomesL.get(0);
                OutcomesL.remove(0);
            }
            else if (ptr.equalsIgnoreCase("Participants")) {
                currSt.participants = ParticipantsL.get(0);
                ParticipantsL.remove(0);
            }
            else if (ptr.equalsIgnoreCase("Label")) {
                currSt.label = LabelL.get(0);
                LabelL.remove(0);
                stuL.add(currSt);
                currSt = new studies();
            }
            else if (ptr.equalsIgnoreCase("Filename")) {
                currFN.fileName = FilenameL.get(0);
                FilenameL.remove(0);
                currFN.stuL = stuL;
                fnL.add(currFN);
                stuL = new ArrayList<studies>();
                currFN = new fName();
            }
        }
        //Uncomment the following for loop to print data structure
        
//        for(fName tempFN : fnL){
//            tempFN.printFName();
//        }
//        
  
        
        //Inclusion Exclusion code starts here
        
        List<String> incl = new ArrayList<String>();
        List<String> excl = new ArrayList<String>();
        for (fName tempFN : fnL) {
            List<studies> stuL1 = tempFN.stuL;
            for(studies st : stuL1){
                System.out.println("<doc>");
                System.out.println("<label>"+st.label+"</label>");
                incl = new ArrayList<String>();
                excl = new ArrayList<String>();
                parseCriteria(st.participants,incl,excl);
                if(!incl.isEmpty()){
                    for (String p : incl) {
                        System.out.println("<inclusion>"+p+"</inclusion>");
                    }
                }    
                if(!excl.isEmpty()){
                    for (String p : excl) {
                        System.out.println("<exclusion>"+p+"</exclusion>");
                    }
                }
                System.out.println("</doc>");
            }
        }

        
        //Inclusion Exclusion code ends here 
        
        
        // Just method to check if everything is parsed
        if((MethodsL.size() + InterventionsL.size() + OutcomesL.size() + ParticipantsL.size() + FilenameL.size()) != 0)
            System.out.println("ERROR : Something not parsed");        
    }
    
    
    
    public static List<String> getValues(String lookFor,String jsonText) throws ParseException{
        List<String> tempL = new ArrayList<String>();
        JSONParser parser = new JSONParser();
        KeyFinder finder = new KeyFinder();
        finder.setMatchKey(lookFor);
        while (!finder.isEnd()) {
            parser.parse(jsonText, finder, true);
            if (finder.isFound()) {
                finder.setFound(false);
                tempL.add((String) finder.getValue());
            }
        }
        System.out.println(lookFor +" Done");
        return tempL;
    }
    
}
public void parseCriteria(String str,List<String> incl, List <String> excl){
//        String str = this.participants;
        if ((str.toLowerCase().contains("inclusion criteria")) && (str.toLowerCase().contains("exclusion criteria"))) {
            Matcher matcher;
            matcher = Pattern.compile("(Inclusion criteria|INCLUSION CRITERIA|inclusion criteria)\\s*(:|\\.)(.*)(Exclusion criteria|EXCLUSION CRITERIA|exclusion criteria)\\s*(:|\\.)(.*)").matcher(str);
            if (matcher.find()) {
                incl.add(matcher.group(3));
                excl.add(matcher.group(6));
            }
        } else if (str.toLowerCase().contains("inclusion criteria")) {
            Matcher matcher1;
            matcher1 = Pattern.compile("(Inclusion criteria|INCLUSION CRITERIA|inclusion criteria)\\s*(:|\\.)(.*)").matcher(str);
            if (matcher1.find()) {
                incl.add(matcher1.group(3));
            }
        }
        else if (str.toLowerCase().contains("exclusion criteria")) {
            Matcher matcher1;
            matcher1 = Pattern.compile("(Exclusion criteria|EXCLUSION CRITERIA|exclusion criteria)\\s*(:|\\.)(.*)").matcher(str);
            if (matcher1.find()) {
                excl.add(matcher1.group(3));
            }
        }
    }