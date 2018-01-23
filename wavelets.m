directory = dir('signaturesTrue/');
threeData10=cell(length(directory),1);

for fileNum = 1:length(directory)
    imageFilename=directory(fileNum).name;
    if(length(strfind(imageFilename,'.png'))>0 || length(strfind(imageFilename,'.jpg'))>0 ) 
        image = imread(strcat('signaturesTrue/',imageFilename));
        imageGrayScale = rgb2gray(image);
        imageBinarized = imbinarize(imageGrayScale);
        
        %figure
        %imshowpair(imageGrayScale,imageBinarized,'montage')
        %title('binarized');
        goodBinarized = zeros(size(imageBinarized,1),size(imageBinarized,2));
        for row=1:size(imageBinarized,1)
            for col=1:size(imageBinarized,2)
                if (imageBinarized(row,col) == 0)
                    goodBinarized(row,col) = 1;
                end
            end
        end
        
        % take into account
        imageWithoutNoise = bwareaopen(goodBinarized,2);
        
        maskForDilatation = strel('square',2);
        imgDilate = imdilate(imageWithoutNoise,maskForDilatation);
        
        %imshowpair(imageWithoutNoise,imgDilate,'montage');
        %title('dilatation');
        
        %[B,L] = bwboundaries(imgDilate,'noholes');
        
        %imshow(label2rgb(L, @jet, [.5 .5 .5]))
        %hold on
        %for k = 1:length(B)
        %   boundary = B{k};
        %   plot(boundary(:,2), boundary(:,1), 'w', 'LineWidth', 2)
        %end
        
        BW = imgDilate;
        [B,L,N,A] = bwboundaries(BW);
        %figure;
        %imshow(BW);
        %title('boundaries');
        %hold on;
        boundaries = {};
        % Loop through object boundaries
        for k = 1:N
            % Boundary k is the parent of a hole if the k-th column
            % of the adjacency matrix A contains a non-zero element
            if nnz(A(:,k)) > 0
                boundary = B{k};
                boundaries{k} = boundary;
                %plot(boundary(:,2), boundary(:,1), 'r', 'LineWidth', 2);
                % Loop through the children of boundary k
                %for l = find(A(:,k))'
                %    boundary = B{l};
                %    plot(boundary(:,2), boundary(:,1), 'g', 'LineWidth', 2);
                %end
            end
        end
        
        clear A;
        
        boundaries = boundaries(~cellfun('isempty',boundaries));
        numberOfClosedBoundaries = size(boundaries,2);
        
        %Test - plotting of boundaries
        coordinates=boundaries{1};
        test = zeros(size(imageBinarized,1),size(imageBinarized,2));
        for row=1:size(coordinates,1)
            test(coordinates(row,1),coordinates(row,2))=1;
        end
        %imshow(test);
        %title('closed contours');
        %End of test
        % Seems to work properly
        
        
        % compute tangential angles
        tangentialAngles = {};
        for bound = 1:numberOfClosedBoundaries
            boundary = boundaries{bound};
            tangentialAngles{bound} = zeros(size(boundary,1),1);
            tangentialAngles{bound}(1) = atan2(boundary(2,1)-boundary(size(boundary,1),1),boundary(2,2)-boundary(size(boundary,2),1));
            for i=2:size(boundary,1)-1
                tangentialAngles{bound}(i) = atan2(boundary(i+1,1)-boundary(i-1,1),boundary(i+1,2)-boundary(i-1,2));
            end
            tangentialAngles{bound}(size(boundary,1)) = atan2(boundary(1,1)-boundary(size(boundary,1)-1,1),boundary(1,2)-boundary(size(boundary,2)-1,1));
            %tangentialAngles{bound} = tangential;
        end
        size(boundary,1);
        
        threeData = {};
        for k=1:numberOfClosedBoundaries
            threeData{k} = [boundaries{k},tangentialAngles{k}];
        end
        %display("boundaries{1}")
        %boundaries{1}
        %display("tanAngles{1}")
        %tangentialAngles{1}
        %display("k")
%k
        threeData10{fileNum}=threeData;
        
        clear bound
        clear BW
        clear coordinates
        clear test
        clear i
        clear col
        clear row
        clear boundary
        clear N
        clear k
        clear L
        clear B
        clear ans
        clear imageGrayScale
        clear imageBinarized
        clear imageWithoutNoise
        clear maskForDilatation
        clear tangentialAngles
        clear imgDilate
        clear boundaries
        
    end
end


threeData10=threeData10(~cellfun('isempty',threeData10));
threeData10
save res.mat threeData10 ;