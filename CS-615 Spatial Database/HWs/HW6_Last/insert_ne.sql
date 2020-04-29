-- In SYS
-- CREATE OR REPLACE DIRECTORY IMGDIR AS '%The folder where the image is%'; 
-- GRANT ALL ON DIRECTORY IMGDIR TO CS615;


DECLARE  
  clobValue HW_NE.DESCRIPTION%TYPE;  
BEGIN  
  clobValue := 'Nebraska locates at the center of USA. The major economy of the state is agriculture. It produces fourth quantity in USA. Nebraska used to be called The Great American Desert because the most of areas of the state are unfit to cultivate. The whole state is arid, plain, and unwooded. The most population of city is not the capital of the state. It is Omaha. One famous landmark in Omaha is Bob Kerrey Pedestrian Bridge. The bridge is a footbridge across the Missouri river between Council Bluffs. Council Bluffs is in Iowa. There are many heritage districts, including Omaha Quartermaster Depot, Field Club, Gold Coast, etc.'; 
  UPDATE HW_NE T SET T.DESCRIPTION = clobValue WHERE T.CAPTIAL='Lincoln';  
  COMMIT;  
END;  
/  

declare  
        finput            bfile;  
        image               blob;  
        srcOffset       integer := 1;  
        dstOffset       integer := 1;  
begin  
        dbms_lob.CreateTemporary( image, true );  
        finput := BFilename( 'IMGDIR', 'flag_ne.png' );  
        dbms_lob.FileOpen( finput, DBMS_LOB.FILE_READONLY );  
  
        dbms_lob.LoadFromFile( image, finput, DBMS_LOB.LOBMAXSIZE, dstOffset, srcOffset );  

        UPDATE HW_NE SET STATE_FLAG=image WHERE HW_NE.CAPTIAL='Lincoln';
        commit;  
  
        dbms_lob.FileClose( finput );  
end;  
/  
