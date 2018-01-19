imageFilename = 'peterDeng.png';
image = imread(imageFilename);
imageGrayScale = rgb2gray(image);
imageBinarized = imbinarize(imageGrayScale);

% imbinarized put almost all coefficients to 1
% this loop does the opposite, after that, the signature is constituted of
% 1 value
goodBinarized = zeros(size(imageBinarized,1),size(imageBinarized,2));
for row=1:size(imageBinarized,1)
    for col=1:size(imageBinarized,2)
        if (imageBinarized(row,col) == 0)
            goodBinarized(row,col) = 1;
        end 
    end
end
%imshow(imageBinarized)
%imshow(goodBinarized)
